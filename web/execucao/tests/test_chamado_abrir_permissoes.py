from __future__ import annotations

from django.contrib.auth import get_user_model
from django.urls import reverse

from execucao.models import Chamado, ExecutionSession
from execucao.tests._base import ChamadoBaseTestCase


class ChamadoAbrirPermissoesTests(ChamadoBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        User = get_user_model()
        self.user = User.objects.create_user(username="u1", password="x")
        self.client.force_login(self.user)

        self.chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            status=Chamado.Status.ABERTO,
        )
        self.url = reverse("execucao:chamado_abrir", kwargs={"chamado_id": self.chamado.id})

    def test_sem_perm_editar_retorna_403_e_nao_cria_sessao(self) -> None:
        resp = self.client.post(self.url)
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(ExecutionSession.objects.count(), 0)
