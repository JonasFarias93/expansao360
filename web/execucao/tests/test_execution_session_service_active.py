from __future__ import annotations

from datetime import timedelta

from django.utils import timezone

from execucao.models import Chamado, ExecutionSession
from execucao.services.execution_session import (
    ActiveSessionConflictError,
    create_active_session,
    get_active_session,
)
from execucao.tests._base import WebAuthBaseTestCase


class ExecutionSessionActiveRuleTests(WebAuthBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            status=Chamado.Status.ABERTO,
        )

    def test_get_active_session_retorna_none_quando_nao_existe(self) -> None:
        assert get_active_session(chamado=self.chamado) is None

    def test_get_active_session_ignora_encerrada(self) -> None:
        ExecutionSession.objects.create(
            chamado=self.chamado,
            usuario=self.user,
            ended_at=timezone.now(),
            ended_reason=ExecutionSession.EndReason.FINALIZADO,
        )
        assert get_active_session(chamado=self.chamado) is None

    def test_get_active_session_ignora_expirada(self) -> None:
        ExecutionSession.objects.create(
            chamado=self.chamado,
            usuario=self.user,
            expires_at=timezone.now() - timedelta(minutes=1),
        )
        assert get_active_session(chamado=self.chamado) is None

    def test_create_active_session_cria_quando_nao_existe_ativa(self) -> None:
        s = create_active_session(chamado=self.chamado, user=self.user)
        assert s.chamado_id == self.chamado.id
        assert s.usuario_id == self.user.id
        assert get_active_session(chamado=self.chamado).id == s.id

    def test_create_active_session_bloqueia_quando_ja_existe_ativa(self) -> None:
        create_active_session(chamado=self.chamado, user=self.user)

        with self.assertRaises(ActiveSessionConflictError):
            create_active_session(chamado=self.chamado, user=self.user)
