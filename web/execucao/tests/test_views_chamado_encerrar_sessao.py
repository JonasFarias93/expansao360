from __future__ import annotations

from django.urls import reverse
from execucao.models import Chamado, ExecutionSession
from execucao.services.execution_session import (
    create_active_session,
    get_active_session,
)
from execucao.tests._base import WebAuthBaseTestCase


class TestChamadoEncerrarSessaoView(WebAuthBaseTestCase):
    def _url(self, cid: int) -> str:
        return reverse("execucao:chamado_encerrar_sessao", kwargs={"chamado_id": cid})

    def setUp(self) -> None:
        super().setUp()
        self.chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            status=Chamado.Status.EM_EXECUCAO,
            tipo=Chamado.Tipo.ENVIO,
        )

    def test_com_sessao_ativa_post_encerrar_entao_encerra(self) -> None:
        create_active_session(chamado=self.chamado, user=self.user)
        self.assertIsNotNone(get_active_session(chamado=self.chamado))

        resp = self.client.post(
            self._url(self.chamado.id),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(resp.status_code, 200)

        self.assertIsNone(get_active_session(chamado=self.chamado))

        last = (
            ExecutionSession.objects.filter(chamado=self.chamado)
            .order_by("-started_at")
            .first()
        )
        self.assertIsNotNone(last)
        assert last is not None
        self.assertIsNotNone(last.ended_at)
        self.assertEqual(last.ended_reason, ExecutionSession.EndReason.USER_EXIT)

    def test_sem_sessao_post_encerrar_entao_e_idempotente(self) -> None:
        self.assertIsNone(get_active_session(chamado=self.chamado))

        resp = self.client.post(
            self._url(self.chamado.id),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(resp.status_code, 200)

        self.assertIsNone(get_active_session(chamado=self.chamado))
