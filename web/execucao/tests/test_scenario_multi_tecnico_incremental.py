from __future__ import annotations

from cadastro.models import Categoria, Equipamento, ItemKit, Kit, TipoEquipamento
from django.contrib.auth import get_user_model
from django.urls import reverse
from execucao.models import Chamado
from execucao.services.execution_session import (
    ActiveSessionConflictError,
    create_active_session,
    get_active_session,
    take_session,
)
from execucao.tests._base import WebAuthBaseTestCase
from iam.execucao_capabilities import CAP_EXECUCAO_SESSAO_TOMAR
from iam.models import Capability, UserCapability

User = get_user_model()


class TestCenarioMultiTecnicoIncremental(WebAuthBaseTestCase):
    def _url(self, cid: int) -> str:
        return reverse(
            "execucao:chamado_salvar_execucao_ajax", kwargs={"chamado_id": cid}
        )

    def _grant_capability(self, user, code: str) -> None:
        cap, _ = Capability.objects.get_or_create(code=code)
        UserCapability.objects.get_or_create(user=user, capability=cap)

    def _kit_gate_nf(self) -> Kit:
        categoria = Categoria.objects.create(nome="Informatica")
        tipo = TipoEquipamento.objects.create(categoria=categoria, nome="TC")
        kit = Kit.objects.create(nome="Kit Gate NF MultiTecnico (tests)")

        eq_rastreavel = Equipamento.objects.create(
            codigo="MICRO_MULTI_TC_TEST",
            nome="Micro TC",
            categoria=categoria,
            tem_ativo=True,
            configuravel=True,
        )
        eq_contavel = Equipamento.objects.create(
            codigo="MOUSE_MULTI_TEST",
            nome="Mouse",
            categoria=categoria,
            tem_ativo=False,
            configuravel=False,
        )

        ItemKit.objects.create(
            kit=kit,
            tipo=tipo,
            equipamento=eq_rastreavel,
            quantidade=1,
            requer_configuracao=False,
        )
        ItemKit.objects.create(
            kit=kit,
            tipo=tipo,
            equipamento=eq_contavel,
            quantidade=1,
            requer_configuracao=False,
        )
        return kit

    def test_tecnico_a_salva_parcial_e_tecnico_b_completa_sem_perder_dados(
        self,
    ) -> None:
        user_b = User.objects.create_user(username="tec_b", password="123")

        self._grant_capability(self.user, "execucao.chamado_editar")
        self._grant_capability(user_b, "execucao.chamado_editar")

        self._grant_capability(user_b, CAP_EXECUCAO_SESSAO_TOMAR)

        kit = self._kit_gate_nf()
        chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=kit,
            status=Chamado.Status.EM_EXECUCAO,
            tipo=Chamado.Tipo.ENVIO,
        )
        chamado.gerar_itens_de_instalacao()

        item_r = chamado.itens.get(tem_ativo=True)
        item_c = chamado.itens.get(tem_ativo=False)

        # ========== Técnico A (self.user) salva parcial ==========
        create_active_session(chamado=chamado, user=self.user)

        resp_a = self.client.post(
            self._url(chamado.id),
            data={
                "contabilidade_numero": "",
                "nf_saida_numero": "",
                f"ativo_{item_r.id}": "ATV-A",
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(resp_a.status_code, 200)

        active_after_a = get_active_session(chamado=chamado)
        self.assertIsNotNone(active_after_a)
        assert active_after_a is not None
        self.assertEqual(active_after_a.usuario_id, self.user.id)

        item_r.refresh_from_db()
        item_c.refresh_from_db()
        self.assertEqual(item_r.ativo, "ATV-A")
        self.assertEqual(item_r.numero_serie, "")
        self.assertIs(item_c.confirmado, False)

        # ========== Técnico B completa ==========
        self.client.force_login(user_b)

        with self.assertRaises(ActiveSessionConflictError):
            create_active_session(chamado=chamado, user=user_b)

        take_session(chamado=chamado, actor=user_b)

        active_now = get_active_session(chamado=chamado)
        self.assertIsNotNone(active_now)
        assert active_now is not None
        self.assertEqual(active_now.usuario_id, user_b.id)

        resp_b = self.client.post(
            self._url(chamado.id),
            data={
                "contabilidade_numero": "",
                "nf_saida_numero": "",
                f"serie_{item_r.id}": "SN-B",
                f"confirmado_{item_c.id}": "on",
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(resp_b.status_code, 200)

        active_after_b = get_active_session(chamado=chamado)
        self.assertIsNotNone(active_after_b)
        assert active_after_b is not None
        self.assertEqual(active_after_b.usuario_id, user_b.id)

        item_r.refresh_from_db()
        item_c.refresh_from_db()

        self.assertEqual(item_r.ativo, "ATV-A")
        self.assertEqual(item_r.numero_serie, "SN-B")
        self.assertIs(item_c.confirmado, True)

        chamado.refresh_from_db()
        self.assertIs(chamado.pode_liberar_nf(), True)
