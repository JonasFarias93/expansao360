from __future__ import annotations

from django.contrib.auth import get_user_model
from django.urls import reverse

from iam.execucao_capabilities import (
    CAP_EXECUCAO_CHAMADO_EDITAR,
    CAP_EXECUCAO_SESSAO_TOMAR,
)
from iam.models import Capability, UserCapability

from execucao.models import Chamado, ExecutionSession, ExecutionSessionLog
from execucao.tests._base import WebAuthBaseTestCase


class TestChamadoTakeSession(WebAuthBaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            status=Chamado.Status.ABERTO,
        )

        self.url_abrir = reverse(
            "execucao:chamado_abrir",
            kwargs={"chamado_id": self.chamado.id},
        )
        self.url_take = reverse(
            "execucao:chamado_take_session",
            kwargs={"chamado_id": self.chamado.id},
        )

        cap_editar, _ = Capability.objects.get_or_create(
            code=CAP_EXECUCAO_CHAMADO_EDITAR
        )
        UserCapability.objects.get_or_create(user=self.user, capability=cap_editar)

        User = get_user_model()
        self.admin = User.objects.create_user(username="admin", password="x")

        cap_take, _ = Capability.objects.get_or_create(code=CAP_EXECUCAO_SESSAO_TOMAR)
        UserCapability.objects.get_or_create(user=self.admin, capability=cap_editar)
        UserCapability.objects.get_or_create(user=self.admin, capability=cap_take)

        self.client_admin = self.client.__class__()
        self.client_admin.force_login(self.admin)

        self.user_b = User.objects.create_user(username="u2", password="x")
        UserCapability.objects.get_or_create(user=self.user_b, capability=cap_editar)
        self.client_b = self.client.__class__()
        self.client_b.force_login(self.user_b)

    def test_quando_admin_toma_sessao_ativa_entao_encerra_antiga_cria_nova_e_registra_log(
        self,
    ) -> None:
        resp = self.client.post(self.url_abrir)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(ExecutionSession.objects.count(), 1)

        old = ExecutionSession.objects.get(chamado=self.chamado, ended_at__isnull=True)
        self.assertEqual(old.usuario_id, self.user.id)

        resp2 = self.client_admin.post(self.url_take)
        self.assertEqual(resp2.status_code, 302)

        self.assertEqual(ExecutionSession.objects.count(), 2)

        old.refresh_from_db()
        self.assertIsNotNone(old.ended_at)
        self.assertEqual(old.ended_reason, "ADMIN_TAKE")

        new = (
            ExecutionSession.objects.filter(chamado=self.chamado)
            .order_by("-started_at")
            .first()
        )
        assert new is not None
        self.assertEqual(new.usuario_id, self.admin.id)
        self.assertIsNone(new.ended_at)

        log = (
            ExecutionSessionLog.objects.filter(chamado=self.chamado)
            .order_by("-created_at")
            .first()
        )
        assert log is not None
        self.assertEqual(log.reason, "ADMIN_TAKE")
        self.assertEqual(log.previous_usuario_id, self.user.id)
        self.assertEqual(log.new_usuario_id, self.admin.id)

    def test_quando_usuario_sem_cap_tomar_entao_retorna_403_e_nao_muda_sessoes(
        self,
    ) -> None:
        self.client.post(self.url_abrir)
        self.assertEqual(ExecutionSession.objects.count(), 1)

        resp = self.client_b.post(self.url_take)
        self.assertEqual(resp.status_code, 403)

        self.assertEqual(ExecutionSession.objects.count(), 1)

    def test_quando_admin_toma_sem_sessao_ativa_entao_retorna_400(self) -> None:
        resp = self.client_admin.post(self.url_take)
        self.assertEqual(resp.status_code, 400)
