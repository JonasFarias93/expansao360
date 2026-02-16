from __future__ import annotations

from cadastro.models import Categoria, Equipamento, ItemKit, Kit, TipoEquipamento
from django.contrib.auth import get_user_model
from django.urls import reverse
from execucao.models import Chamado
from execucao.services.execution_session import (
    create_active_session,
    get_active_session,
)
from execucao.tests._base import WebAuthBaseTestCase
from iam.models import Capability, UserCapability

User = get_user_model()


class TestCenarioMultiTecnicoIncremental(WebAuthBaseTestCase):
    def _url(self, cid: int) -> str:
        return reverse(
            "execucao:chamado_salvar_execucao_ajax", kwargs={"chamado_id": cid}
        )

    def _grant_edit_capability(self, user) -> None:
        cap, _ = Capability.objects.get_or_create(code="execucao.chamado_editar")
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
        # técnico B
        user_b = User.objects.create_user(username="tec_b", password="123")

        # Garantir capability para A e B (o foco do teste é fluxo incremental, não IAM)
        self._grant_edit_capability(self.user)
        self._grant_edit_capability(user_b)

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
                # serie não enviada (parcial)
                # contável não confirmado ainda
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(resp_a.status_code, 200)
        self.assertIsNone(get_active_session(chamado=chamado))

        item_r.refresh_from_db()
        item_c.refresh_from_db()
        self.assertEqual(item_r.ativo, "ATV-A")
        self.assertEqual(item_r.numero_serie, "")  # ainda vazio
        self.assertIs(item_c.confirmado, False)

        # ========== Técnico B completa ==========
        self.client.force_login(user_b)
        create_active_session(chamado=chamado, user=user_b)

        resp_b = self.client.post(
            self._url(chamado.id),
            data={
                "contabilidade_numero": "",
                "nf_saida_numero": "",
                # não reenviar ativo (não pode apagar/alterar sem querer)
                f"serie_{item_r.id}": "SN-B",
                f"confirmado_{item_c.id}": "on",
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(resp_b.status_code, 200)
        self.assertIsNone(get_active_session(chamado=chamado))

        item_r.refresh_from_db()
        item_c.refresh_from_db()

        # garante que ativo do A foi preservado
        self.assertEqual(item_r.ativo, "ATV-A")
        self.assertEqual(item_r.numero_serie, "SN-B")
        self.assertIs(item_c.confirmado, True)

        chamado.refresh_from_db()
        self.assertIs(chamado.pode_liberar_nf(), True)
