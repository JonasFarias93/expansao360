from __future__ import annotations

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone

from chamados.models import Chamado
from chamados.selectors.fila import get_active_sessions_by_chamado
from execucao.models import ExecutionSession

from ._base import ChamadoBaseTestCase


class TestFilaActiveSessionsSelector(ChamadoBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        User = get_user_model()
        self.user = User.objects.create_user(username="sess-user", password="x")

    def _mk_chamado(self, *, protocolo: str) -> Chamado:
        return Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            tipo=Chamado.Tipo.ENVIO,
            status=Chamado.Status.ABERTO,
            protocolo=protocolo,
        )

    def test_dado_sessoes_quando_buscar_entao_retorna_apenas_ativas_e_ignora_expiradas_e_ended(
        self,
    ) -> None:
        now = timezone.now()

        ch1 = self._mk_chamado(protocolo="S-1")
        ch2 = self._mk_chamado(protocolo="S-2")

        # ch1: ended -> ignorar
        ExecutionSession.objects.create(
            chamado=ch1,
            usuario=self.user,
            started_at=now - timedelta(minutes=30),
            expires_at=now + timedelta(hours=1),
            ended_at=now - timedelta(minutes=10),
        )

        # ch1: expirada -> ignorar (ended_at NULL mas expires_at <= now)
        ExecutionSession.objects.create(
            chamado=ch1,
            usuario=self.user,
            started_at=now - timedelta(minutes=20),
            expires_at=now - timedelta(seconds=1),
            ended_at=now - timedelta(seconds=1),  # garante que não viola unique open
        )

        # ch1: ativa única (deve aparecer)
        s_active = ExecutionSession.objects.create(
            chamado=ch1,
            usuario=self.user,
            started_at=now - timedelta(minutes=5),
            expires_at=now + timedelta(hours=1),
        )

        # ch2: ativa única
        s2 = ExecutionSession.objects.create(
            chamado=ch2,
            usuario=self.user,
            started_at=now - timedelta(minutes=7),
            expires_at=now + timedelta(hours=1),
        )

        out = get_active_sessions_by_chamado([ch1.id, ch2.id], now=now)

        assert out[ch1.id].id == s_active.id
        assert out[ch2.id].id == s2.id
