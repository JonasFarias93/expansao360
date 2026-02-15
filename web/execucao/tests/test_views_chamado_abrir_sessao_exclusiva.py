from __future__ import annotations

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from iam.execucao_capabilities import CAP_EXECUCAO_CHAMADO_EDITAR
from iam.models import Capability, UserCapability

from execucao.models import Chamado, ExecutionSession
from execucao.tests._base import WebAuthBaseTestCase


class TestChamadoAbrirSessaoExclusiva(WebAuthBaseTestCase):
    """
    Contratos mínimos da sessão exclusiva ao abrir chamado:

    - técnico A abre -> cria sessão
    - técnico A abre de novo -> reentra (não cria outra)
    - técnico B tenta abrir -> bloqueia (não cria outra)
    - sessão encerrada manualmente -> técnico B consegue abrir

    Premissa: ambos os técnicos possuem CAP_EXECUCAO_CHAMADO_EDITAR,
    pois o endpoint /chamado_abrir é protegido por IAM (403 sem a cap).
    """

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

        User = get_user_model()
        self.user_b = User.objects.create_user(username="u2", password="x")

        cap, _ = Capability.objects.get_or_create(code=CAP_EXECUCAO_CHAMADO_EDITAR)
        UserCapability.objects.get_or_create(user=self.user, capability=cap)
        UserCapability.objects.get_or_create(user=self.user_b, capability=cap)

        self.client_b = self.client.__class__()
        self.client_b.force_login(self.user_b)

    def test_quando_tecnico_a_abre_entao_cria_sessao(self) -> None:
        resp = self.client.post(self.url_abrir)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(ExecutionSession.objects.count(), 1)

        s = ExecutionSession.objects.get(chamado=self.chamado)
        self.assertEqual(s.usuario_id, self.user.id)
        self.assertIsNone(s.ended_at)

    def test_quando_tecnico_a_abre_novamente_entao_reentra_sem_criar_nova(self) -> None:
        self.client.post(self.url_abrir)
        self.assertEqual(ExecutionSession.objects.count(), 1)

        resp = self.client.post(self.url_abrir)
        self.assertEqual(resp.status_code, 302)

        self.assertEqual(ExecutionSession.objects.count(), 1)

        s = ExecutionSession.objects.get(chamado=self.chamado)
        self.assertEqual(s.usuario_id, self.user.id)
        self.assertIsNone(s.ended_at)

    def test_quando_tecnico_b_tenta_com_sessao_ativa_entao_bloqueia_sem_criar_nova(
        self,
    ) -> None:
        self.client.post(self.url_abrir)
        self.assertEqual(ExecutionSession.objects.count(), 1)

        resp = self.client_b.post(self.url_abrir)
        self.assertEqual(resp.status_code, 302)

        self.assertEqual(ExecutionSession.objects.count(), 1)
        s = ExecutionSession.objects.get(chamado=self.chamado)
        self.assertEqual(s.usuario_id, self.user.id)

    def test_quando_sessao_encerrada_entao_tecnico_b_consegue_criar_nova(self) -> None:
        self.client.post(self.url_abrir)
        s = ExecutionSession.objects.get(chamado=self.chamado)

        s.ended_at = timezone.now()
        s.ended_reason = ExecutionSession.EndReason.FINALIZADO
        s.save(update_fields=["ended_at", "ended_reason"])

        resp = self.client_b.post(self.url_abrir)
        self.assertEqual(resp.status_code, 302)

        self.assertEqual(ExecutionSession.objects.count(), 2)

        new_s = (
            ExecutionSession.objects.filter(chamado=self.chamado)
            .order_by("-started_at")
            .first()
        )
        assert new_s is not None
        self.assertEqual(new_s.usuario_id, self.user_b.id)
        self.assertIsNone(new_s.ended_at)
