from __future__ import annotations

from django.urls import reverse
from django.utils import timezone

from execucao.models import Chamado
from execucao.services.execution_session import create_active_session
from execucao.tests._base import WebAuthBaseTestCase, grant_cap


class ChamadoFinalizarViewTests(WebAuthBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.url = lambda cid: reverse("execucao:chamado_finalizar", kwargs={"chamado_id": cid})

    def _mk_chamado(self, **kwargs) -> Chamado:
        data = dict(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            tipo=Chamado.Tipo.ENVIO,
            status=Chamado.Status.AGUARDANDO_COLETA,
            contabilidade_numero="123",
            nf_saida_numero="999",
            coleta_confirmada_em=timezone.now(),
        )
        data.update(kwargs)
        return Chamado.objects.create(**data)

    def test_sem_sessao_retorna_403(self):
        chamado = self._mk_chamado()

        # garante cap (compat com teu IAM)
        grant_cap(self.user, "execucao.chamado_finalizar")
        grant_cap(self.user, "execucao.chamado.finalizar")

        resp = self.client.post(self.url(chamado.id))
        self.assertEqual(resp.status_code, 403)

    def test_com_pendencias_retorna_400_ajax(self):
        chamado = self._mk_chamado(coleta_confirmada_em=None)  # pendência de coleta
        create_active_session(chamado=chamado, user=self.user)

        grant_cap(self.user, "execucao.chamado_finalizar")
        grant_cap(self.user, "execucao.chamado.finalizar")

        resp = self.client.post(
            self.url(chamado.id),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(resp.status_code, 400)

        chamado.refresh_from_db()
        self.assertNotEqual(chamado.status, Chamado.Status.FINALIZADO)

    def test_finaliza_muda_status_e_encerra_sessao(self):
        chamado = self._mk_chamado()
        sessao = create_active_session(chamado=chamado, user=self.user)

        grant_cap(self.user, "execucao.chamado_finalizar")
        grant_cap(self.user, "execucao.chamado.finalizar")

        resp = self.client.post(self.url(chamado.id))
        self.assertEqual(resp.status_code, 302)

        chamado.refresh_from_db()
        self.assertEqual(chamado.status, Chamado.Status.FINALIZADO)

        sessao.refresh_from_db()
        self.assertIsNotNone(sessao.ended_at)
        self.assertEqual(sessao.ended_reason, "FINALIZE")
