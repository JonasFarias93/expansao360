from __future__ import annotations

from django.contrib.auth import get_user_model
from django.urls import reverse

from execucao.models import Chamado, ExecutionSession
from execucao.tests._base import WebAuthBaseTestCase


class ChamadoAbrirIniciaSessaoTests(WebAuthBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            status=Chamado.Status.ABERTO,
        )

    def test_abrir_cria_sessao_e_redireciona_para_setup_quando_aberto(self) -> None:
        url = reverse("execucao:chamado_abrir", kwargs={"chamado_id": self.chamado.id})
        resp = self.client.post(url)

        self.assertEqual(ExecutionSession.objects.count(), 1)
        sess = ExecutionSession.objects.first()
        assert sess is not None
        self.assertEqual(sess.chamado_id, self.chamado.id)
        self.assertEqual(sess.usuario_id, self.user.id)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(
            resp["Location"],
            reverse("execucao:chamado_setup", kwargs={"chamado_id": self.chamado.id}),
        )

    def test_abrir_reentra_quando_mesmo_usuario(self) -> None:
        ExecutionSession.objects.create(chamado=self.chamado, usuario=self.user)

        url = reverse("execucao:chamado_abrir", kwargs={"chamado_id": self.chamado.id})
        resp = self.client.post(url)

        self.assertEqual(ExecutionSession.objects.count(), 1)
        self.assertEqual(resp.status_code, 302)

    def test_abrir_bloqueia_quando_outro_usuario(self) -> None:
        User = get_user_model()
        other = User.objects.create_user(username="u2", password="x")

        ExecutionSession.objects.create(chamado=self.chamado, usuario=other)

        url = reverse("execucao:chamado_abrir", kwargs={"chamado_id": self.chamado.id})
        resp = self.client.post(url)

        self.assertEqual(ExecutionSession.objects.count(), 1)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(
            resp["Location"],
            reverse("execucao:chamado_detalhe", kwargs={"chamado_id": self.chamado.id}),
        )
