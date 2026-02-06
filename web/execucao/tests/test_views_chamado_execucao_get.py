# web/execucao/tests/test_views_chamado_execucao_get.py
from __future__ import annotations

from django.urls import reverse

from execucao.models import Chamado

from ._base import WebAuthBaseTestCase, grant_cap


class ChamadoExecucaoGetWebTest(WebAuthBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        grant_cap(self.user, "execucao.chamado.visualizar")

    def test_get_chamado_detalhe_redirect_para_setup_quando_em_abertura(self) -> None:
        chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            status=Chamado.Status.EM_ABERTURA,
        )

        url = reverse("execucao:chamado_detalhe", args=[chamado.id])
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, reverse("execucao:chamado_setup", args=[chamado.id]))

    def test_get_chamado_detalhe_renderiza_execucao_quando_aberto(self) -> None:
        chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            status=Chamado.Status.ABERTO,  # ✅ conforme seu conceito
        )

        url = reverse("execucao:chamado_detalhe", args=[chamado.id])
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "execucao/chamado_execucao.html")
        self.assertIn("chamado", resp.context)
        self.assertEqual(resp.context["chamado"].id, chamado.id)

    def test_get_execucao_inclui_script_chamado_detalhe_js(self) -> None:
        chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            status=Chamado.Status.ABERTO,
        )

        url = reverse("execucao:chamado_detalhe", args=[chamado.id])
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        html = resp.content.decode("utf-8")
        self.assertIn("execucao/js/chamado_detalhe.js", html)
