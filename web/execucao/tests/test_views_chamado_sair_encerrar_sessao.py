from __future__ import annotations

from django.urls import reverse
from execucao.models import Chamado
from execucao.services.execution_session import (
    create_active_session,
    get_active_session,
)
from execucao.tests._base import WebAuthBaseTestCase


class TestChamadoSairEncerrarSessaoView(WebAuthBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            status=Chamado.Status.EM_EXECUCAO,
            tipo=Chamado.Tipo.ENVIO,
        )

    def test_quando_clica_voltar_entao_encerra_sessao_e_redireciona_para_fila(
        self,
    ) -> None:
        create_active_session(chamado=self.chamado, user=self.user)
        self.assertIsNotNone(get_active_session(chamado=self.chamado))

        url = reverse(
            "execucao:chamado_encerrar_sessao", kwargs={"chamado_id": self.chamado.id}
        )
        next_url = reverse("execucao:fila")

        resp = self.client.post(f"{url}?next={next_url}")
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, next_url)

        self.assertIsNone(get_active_session(chamado=self.chamado))

    def test_quando_sem_sessao_voltar_e_idempotente_e_redireciona(self) -> None:
        self.assertIsNone(get_active_session(chamado=self.chamado))

        url = reverse(
            "execucao:chamado_encerrar_sessao", kwargs={"chamado_id": self.chamado.id}
        )
        next_url = reverse("execucao:fila")

        resp = self.client.post(f"{url}?next={next_url}")
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, next_url)

        self.assertIsNone(get_active_session(chamado=self.chamado))
