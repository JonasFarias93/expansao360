from __future__ import annotations

from datetime import timedelta

from django.db import IntegrityError
from django.utils import timezone

from execucao.models import Chamado, ExecutionSession
from execucao.tests._base import WebAuthBaseTestCase


class ExecutionSessionModelTests(WebAuthBaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            status=Chamado.Status.ABERTO,
        )

    def test_execution_session_queryset_active_filtra_por_ended_at_e_expires_at(self) -> None:
        # s1: aberta e ativa
        s1 = ExecutionSession.objects.create(chamado=self.chamado, usuario=self.user)

        # s2: encerrada
        s2 = ExecutionSession.objects.create(
            chamado=self.chamado,
            usuario=self.user,
            ended_at=timezone.now(),
            ended_reason=ExecutionSession.EndReason.FINALIZADO,
        )

        # encerra s1 para permitir criar uma nova sessão aberta (constraint)
        s1.ended_at = timezone.now()
        s1.ended_reason = ExecutionSession.EndReason.OUTRO
        s1.save(update_fields=["ended_at", "ended_reason"])

        # s3: aberta, mas expirada (portanto NÃO ativa)
        s3 = ExecutionSession.objects.create(
            chamado=self.chamado,
            usuario=self.user,
            expires_at=timezone.now() - timedelta(minutes=1),
        )

        active = ExecutionSession.objects.active()
        self.assertNotIn(s2, active)  # encerrada
        self.assertNotIn(s3, active)  # expirada

    def test_execution_session_unique_constraint_impede_duas_sessoes_ativas_mesmo_chamado(
        self,
    ) -> None:
        ExecutionSession.objects.create(chamado=self.chamado, usuario=self.user)

        with self.assertRaises(IntegrityError):
            ExecutionSession.objects.create(chamado=self.chamado, usuario=self.user)
