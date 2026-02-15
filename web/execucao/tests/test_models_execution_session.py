from __future__ import annotations

from datetime import timedelta

from django.db import IntegrityError, transaction
from django.utils import timezone

from execucao.models import Chamado, ExecutionSession
from execucao.tests._base import WebAuthBaseTestCase


class TestExecutionSessionModel(WebAuthBaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            status=Chamado.Status.ABERTO,
        )

    def test_quando_sessao_encerrada_ou_expirada_entao_nao_aparece_em_active(
        self,
    ) -> None:
        # Mantém uma sessão realmente ativa em OUTRO chamado
        outro_chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            status=Chamado.Status.ABERTO,
        )
        s_ativa = ExecutionSession.objects.create(
            chamado=outro_chamado, usuario=self.user
        )

        # Sessão encerrada (não deve ser ativa)
        s_encerrada = ExecutionSession.objects.create(
            chamado=self.chamado,
            usuario=self.user,
            ended_at=timezone.now(),
            ended_reason=ExecutionSession.EndReason.FINALIZADO,
        )

        # Para criar uma sessão "aberta porém expirada" no mesmo chamado,
        # precisamos garantir que não exista outra aberta (constraint).
        s_temp = ExecutionSession.objects.create(
            chamado=self.chamado, usuario=self.user
        )
        s_temp.ended_at = timezone.now()
        s_temp.ended_reason = ExecutionSession.EndReason.OUTRO
        s_temp.save(update_fields=["ended_at", "ended_reason"])

        s_expirada = ExecutionSession.objects.create(
            chamado=self.chamado,
            usuario=self.user,
            expires_at=timezone.now() - timedelta(minutes=1),
        )

        active = list(ExecutionSession.objects.active())

        assert s_ativa in active
        assert s_encerrada not in active
        assert s_expirada not in active

    def test_quando_existe_sessao_aberta_no_chamado_entao_nao_permite_outra_sessao_aberta(
        self,
    ) -> None:
        ExecutionSession.objects.create(chamado=self.chamado, usuario=self.user)

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                ExecutionSession.objects.create(chamado=self.chamado, usuario=self.user)
