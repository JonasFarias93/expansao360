from __future__ import annotations

from cadastro.models import Categoria, Equipamento, ItemKit, Kit, TipoEquipamento
from django.urls import reverse
from execucao.models import Chamado, ExecutionSession
from execucao.services.execution_session import (
    create_active_session,
    get_active_session,
)
from execucao.tests._base import WebAuthBaseTestCase


class TestChamadoSalvarExecucaoAjaxView(WebAuthBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self._url = lambda cid: reverse(
            "execucao:chamado_salvar_execucao", kwargs={"chamado_id": cid}
        )

        self.chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            status=Chamado.Status.ABERTO,
            tipo=Chamado.Tipo.ENVIO,
        )

    def _setup_kit_com_itens_gate_nf(self) -> Kit:
        """Cria kit que gera itens (rastreável + contável) para habilitar o gate de NF."""
        categoria = Categoria.objects.create(nome="Informatica")
        tipo = TipoEquipamento.objects.create(categoria=categoria, nome="TC")
        kit = Kit.objects.create(nome="Kit Gate NF (tests)")

        eq_rastreavel = Equipamento.objects.create(
            codigo="MICRO_TC_TEST",
            nome="Micro TC",
            categoria=categoria,
            tem_ativo=True,
            configuravel=True,
        )
        eq_contavel = Equipamento.objects.create(
            codigo="MOUSE_TEST",
            nome="Mouse",
            categoria=categoria,
            tem_ativo=False,
            configuravel=False,
        )

        ItemKit.objects.create(
            kit=kit,
            tipo=tipo,
            equipamento=eq_rastreavel,
            quantidade=2,
            requer_configuracao=False,
        )
        ItemKit.objects.create(
            kit=kit,
            tipo=tipo,
            equipamento=eq_contavel,
            quantidade=2,
            requer_configuracao=False,
        )
        return kit

    def _ensure_itens_gerados(self, chamado: Chamado) -> None:
        if not chamado.itens.exists():
            chamado.gerar_itens_de_instalacao()

    def _deixar_itens_ok_para_gate_nf(self, chamado: Chamado) -> None:
        """Deixa os itens do chamado aptos para `pode_liberar_nf()`."""
        self._ensure_itens_gerados(chamado)

        for item in chamado.itens.all():
            if item.tem_ativo:
                item.ativo = "ATV-123"
                item.numero_serie = "SN-123"
                item.save(update_fields=["ativo", "numero_serie"])
            else:
                item.confirmado = True
                item.save(update_fields=["confirmado"])

        assert chamado.pode_liberar_nf() is True

    def test_quando_salvar_sem_sessao_entao_retorna_403(self) -> None:
        resp = self.client.post(
            self._url(self.chamado.id),
            data={"contabilidade_numero": "PED-001", "nf_saida_numero": ""},
        )
        self.assertEqual(resp.status_code, 403)

    def test_quando_primeiro_save_aberto_entao_promove_em_execucao_e_encerra_sessao_save(
        self,
    ) -> None:
        create_active_session(chamado=self.chamado, user=self.user)

        resp = self.client.post(
            self._url(self.chamado.id),
            data={"contabilidade_numero": "", "nf_saida_numero": ""},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(resp.status_code, 200)

        self.chamado.refresh_from_db()
        self.assertEqual(str(self.chamado.status), str(Chamado.Status.EM_EXECUCAO))

        self.assertIsNone(get_active_session(chamado=self.chamado))

        last = (
            ExecutionSession.objects.filter(chamado=self.chamado)
            .order_by("-started_at")
            .first()
        )
        self.assertIsNotNone(last)
        assert last is not None
        self.assertIsNotNone(last.ended_at)
        self.assertEqual(last.ended_reason, ExecutionSession.EndReason.SAVE)

    def test_quando_gate_nf_ok_e_contabil_preenchido_entao_promove_aguardando_nf_e_encerra_sessao(
        self,
    ) -> None:
        kit = self._setup_kit_com_itens_gate_nf()

        chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=kit,
            status=Chamado.Status.EM_EXECUCAO,
            tipo=Chamado.Tipo.ENVIO,
        )

        create_active_session(chamado=chamado, user=self.user)

        self._deixar_itens_ok_para_gate_nf(chamado)
        chamado.contabilidade_numero = "PED-001"
        chamado.save(update_fields=["contabilidade_numero"])

        resp = self.client.post(
            self._url(chamado.id),
            data={"contabilidade_numero": "PED-001", "nf_saida_numero": ""},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(resp.status_code, 200)

        chamado.refresh_from_db()
        self.assertEqual(str(chamado.status), str(Chamado.Status.AGUARDANDO_NF))

        self.assertIsNone(get_active_session(chamado=chamado))

    def test_quando_nf_saida_preenchida_entao_promove_aguardando_coleta_e_encerra_sessao(
        self,
    ) -> None:
        chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            status=Chamado.Status.EM_EXECUCAO,
            tipo=Chamado.Tipo.ENVIO,
        )

        create_active_session(chamado=chamado, user=self.user)

        resp = self.client.post(
            self._url(chamado.id),
            data={"contabilidade_numero": "", "nf_saida_numero": "12345"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(resp.status_code, 200)

        chamado.refresh_from_db()
        self.assertEqual(str(chamado.status), str(Chamado.Status.AGUARDANDO_COLETA))

        self.assertIsNone(get_active_session(chamado=chamado))

    def test_quando_item_configurado_entao_promove_em_configuracao_e_encerra_sessao(
        self,
    ) -> None:
        kit = self._setup_kit_com_itens_gate_nf()

        chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=kit,
            status=Chamado.Status.EM_EXECUCAO,
            tipo=Chamado.Tipo.ENVIO,
        )

        self._ensure_itens_gerados(chamado)
        item = chamado.itens.first()
        assert item is not None

        create_active_session(chamado=chamado, user=self.user)

        url_cfg = reverse("execucao:item_configurar", args=[item.id])
        resp = self.client.post(url_cfg)
        self.assertEqual(resp.status_code, 200)

        resp2 = self.client.post(
            self._url(chamado.id),
            data={"contabilidade_numero": "", "nf_saida_numero": ""},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(resp2.status_code, 200)

        chamado.refresh_from_db()
        self.assertEqual(str(chamado.status), str(Chamado.Status.EM_CONFIGURACAO))

        self.assertIsNone(get_active_session(chamado=chamado))
