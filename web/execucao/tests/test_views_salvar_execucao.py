from __future__ import annotations

from execucao.models import Chamado, ExecutionSession
from execucao.services.execution_session import create_active_session, get_active_session
from execucao.tests._base import WebAuthBaseTestCase


class ChamadoSalvarExecucaoViewTests(WebAuthBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            status="ABERTO",
            tipo=Chamado.Tipo.ENVIO,
        )

    def test_post_sem_sessao_ativa_retorna_403(self) -> None:
        resp = self.client.post(
            f"/execucao/chamados/{self.chamado.id}/salvar/",
            data={"contabilidade_numero": "PED-001", "nf_saida_numero": ""},
        )
        self.assertEqual(resp.status_code, 403)

    def test_post_com_sessao_ativa_recalcula_status_e_encerra_sessao_save(self) -> None:
        create_active_session(chamado=self.chamado, user=self.user)

        resp = self.client.post(
            f"/execucao/chamados/{self.chamado.id}/salvar/",
            data={"contabilidade_numero": "PED-001", "nf_saida_numero": ""},
        )
        self.assertEqual(resp.status_code, 302)

        self.chamado.refresh_from_db()
        # primeiro salvar: ABERTO -> EM_EXECUCAO
        self.assertEqual(str(self.chamado.status), "EM_EXECUCAO")

        sess = get_active_session(chamado=self.chamado)
        self.assertIsNone(sess)  # não deve existir ativa

        # valida a última sessão encerrada
        last = ExecutionSession.objects.filter(chamado=self.chamado).order_by("-started_at").first()
        self.assertIsNotNone(last)
        assert last is not None
        self.assertIsNotNone(last.ended_at)
        self.assertEqual(last.ended_reason, ExecutionSession.EndReason.SAVE)
