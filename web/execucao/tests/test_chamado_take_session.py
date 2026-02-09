from __future__ import annotations

from django.contrib.auth import get_user_model
from django.urls import reverse
from iam.execucao_capabilities import CAP_EXECUCAO_CHAMADO_EDITAR, CAP_EXECUCAO_SESSAO_TOMAR
from iam.models import Capability, UserCapability

from execucao.models import Chamado, ExecutionSession, ExecutionSessionLog
from execucao.tests._base import WebAuthBaseTestCase


class ChamadoTakeSessionTests(WebAuthBaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        # Chamado base
        self.chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            status=Chamado.Status.ABERTO,
        )

        self.url_abrir = reverse("execucao:chamado_abrir", kwargs={"chamado_id": self.chamado.id})
        self.url_take = reverse(
            "execucao:chamado_take_session",
            kwargs={"chamado_id": self.chamado.id},
        )

        # User comum (self.user) precisa da cap de editar pra abrir sessão
        cap_editar, _ = Capability.objects.get_or_create(code=CAP_EXECUCAO_CHAMADO_EDITAR)
        UserCapability.objects.get_or_create(user=self.user, capability=cap_editar)

        # Admin
        User = get_user_model()
        self.admin = User.objects.create_user(username="admin", password="x")

        # Admin precisa de editar (para fluxo pós-take) e sessao_tomar (pra tomar)
        cap_take, _ = Capability.objects.get_or_create(code=CAP_EXECUCAO_SESSAO_TOMAR)
        UserCapability.objects.get_or_create(user=self.admin, capability=cap_editar)
        UserCapability.objects.get_or_create(user=self.admin, capability=cap_take)

        self.client_admin = self.client.__class__()
        self.client_admin.force_login(self.admin)

        # Cliente "não-admin" (usuário B) para testar 403
        self.user_b = User.objects.create_user(username="u2", password="x")
        UserCapability.objects.get_or_create(user=self.user_b, capability=cap_editar)
        self.client_b = self.client.__class__()
        self.client_b.force_login(self.user_b)

    def test_admin_toma_sessao_ativa_cria_nova_e_encerra_antiga(self) -> None:
        # técnico (self.user) abre -> cria sessão ativa
        resp = self.client.post(self.url_abrir)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(ExecutionSession.objects.count(), 1)

        old = ExecutionSession.objects.get(chamado=self.chamado, ended_at__isnull=True)
        self.assertEqual(old.usuario_id, self.user.id)

        # admin toma
        resp2 = self.client_admin.post(self.url_take)
        self.assertEqual(resp2.status_code, 302)

        self.assertEqual(ExecutionSession.objects.count(), 2)

        # antiga encerrada como ADMIN_TAKE
        old.refresh_from_db()
        self.assertIsNotNone(old.ended_at)
        self.assertEqual(old.ended_reason, "ADMIN_TAKE")

        # nova sessão ativa para admin
        new = ExecutionSession.objects.filter(chamado=self.chamado).order_by("-started_at").first()
        assert new is not None
        self.assertEqual(new.usuario_id, self.admin.id)
        self.assertIsNone(new.ended_at)

        # auditoria mínima
        log = (
            ExecutionSessionLog.objects.filter(chamado=self.chamado).order_by("-created_at").first()
        )
        assert log is not None
        self.assertEqual(log.reason, "ADMIN_TAKE")
        self.assertEqual(log.previous_usuario_id, self.user.id)
        self.assertEqual(log.new_usuario_id, self.admin.id)

    def test_usuario_comum_tenta_tomar_retorna_403(self) -> None:
        # cria sessão ativa com self.user
        self.client.post(self.url_abrir)
        self.assertEqual(ExecutionSession.objects.count(), 1)

        # user_b não tem sessao_tomar -> 403
        resp = self.client_b.post(self.url_take)
        self.assertEqual(resp.status_code, 403)

        # não altera sessões
        self.assertEqual(ExecutionSession.objects.count(), 1)

    def test_tomar_sem_sessao_retorna_400(self) -> None:
        # sem sessão aberta
        resp = self.client_admin.post(self.url_take)
        self.assertEqual(resp.status_code, 400)
