from __future__ import annotations

from django.urls import reverse
from execucao.models import Chamado

from ._base import WebAuthBaseTestCase, grant_cap


class TestChamadoDetalheGetView(WebAuthBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        grant_cap(self.user, "execucao.chamado.visualizar")

    def test_quando_em_abertura_entao_redireciona_para_setup(self) -> None:
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

    def test_quando_aberto_entao_renderiza_template_execucao_com_contexto(self) -> None:
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
        self.assertTemplateUsed(resp, "execucao/chamado_execucao.html")
        self.assertIn("chamado", resp.context)
        self.assertEqual(resp.context["chamado"].id, chamado.id)

    def test_quando_renderiza_execucao_entao_inclui_script_execucao_detalhe_js(
        self,
    ) -> None:
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
        self.assertIn("execucao/js/execucao_detalhe.js", html)

    def test_quando_renderiza_execucao_entao_expoe_execution_root_data_attrs_contract(
        self,
    ) -> None:
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

        self.assertIn('id="execution-root"', html)
        self.assertIn("data-has-session=", html)
        self.assertIn("data-can-edit=", html)
        self.assertIn("data-can-finalize=", html)
