from django.urls import reverse

from execucao.models import Chamado
from execucao.tests._base import WebAuthBaseTestCase, grant_cap


class HistoricoFiltroJavaTests(WebAuthBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        grant_cap(self.user, "execucao.chamado.visualizar")

    def test_historico_busca_por_java_codigo(self) -> None:
        self.loja.codigo = "02"
        self.loja.nome = "Teste Loja"
        self.loja.save()

        loja_12 = self.loja.__class__.objects.create(codigo="12", nome="Loja 12")

        c1 = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            status="ABERTO",
        )
        c2 = Chamado.objects.create(
            loja=loja_12,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            status="ABERTO",
        )

        url = reverse("execucao:historico")
        resp = self.client.get(url, {"java": "02"})

        self.assertEqual(resp.status_code, 200)

        html = resp.content.decode("utf-8")
        self.assertIn(c1.protocolo, html)
        self.assertNotIn(c2.protocolo, html)
