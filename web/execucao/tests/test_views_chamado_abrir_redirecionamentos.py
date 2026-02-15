from __future__ import annotations

from django.contrib.auth import get_user_model
from django.urls import reverse

from execucao.models import Chamado, ExecutionSession
from execucao.tests._base import WebAuthBaseTestCase


class TestChamadoAbrirRedirecionamentos(WebAuthBaseTestCase):
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

    def test_quando_abre_chamado_aberto_entao_cria_sessao_e_redireciona_setup(
        self,
    ) -> None:
        resp = self.client.post(self.url_abrir)

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

    def test_quando_reentra_mesmo_usuario_entao_redireciona_e_nao_cria_nova_sessao(
        self,
    ) -> None:
        ExecutionSession.objects.create(chamado=self.chamado, usuario=self.user)

        resp = self.client.post(self.url_abrir)

        self.assertEqual(ExecutionSession.objects.count(), 1)
        self.assertEqual(resp.status_code, 302)

    def test_quando_sessao_ativa_de_outro_usuario_entao_redireciona_detalhe_e_nao_cria_nova(
        self,
    ) -> None:
        User = get_user_model()
        other = User.objects.create_user(username="u2", password="x")

        ExecutionSession.objects.create(chamado=self.chamado, usuario=other)

        resp = self.client.post(self.url_abrir)

        self.assertEqual(ExecutionSession.objects.count(), 1)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(
            resp["Location"],
            reverse("execucao:chamado_detalhe", kwargs={"chamado_id": self.chamado.id}),
        )
