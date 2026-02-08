from django.urls import reverse
from execucao.tests._base import WebAuthBaseTestCase, grant_cap

from cadastro.models import Loja


class LojaListBuscaTests(WebAuthBaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        # garante acesso ao endpoint de cadastro (GET list)
        grant_cap(self.user, "cadastro.visualizar")

        # limpa a loja criada no base para não poluir asserts (opcional, mas ajuda)
        Loja.objects.all().delete()

        Loja.objects.create(
            codigo="01", nome="Loja Paulista", hist="H123", cidade="São Paulo", uf="SP"
        )
        Loja.objects.create(
            codigo="02", nome="Loja Centro", hist="PAULISTA-99", cidade="Campinas", uf="SP"
        )
        Loja.objects.create(
            codigo="03", nome="Loja Rio", hist="H000", cidade="Rio de Janeiro", uf="RJ"
        )

    def test_busca_filtra_resultados_por_q(self) -> None:
        url = reverse("registry:loja_list")
        resp = self.client.get(url, {"q": "paulista", "per_page": "25"})
        self.assertEqual(resp.status_code, 200)

        content = resp.content.decode("utf-8")
        self.assertIn("Loja Paulista", content)
        self.assertIn("Loja Centro", content)
        self.assertNotIn("Loja Rio", content)

    def test_paginacao_preserva_q(self) -> None:
        for i in range(30):
            Loja.objects.create(
                codigo=f"9{i}",
                nome=f"Loja Paulista Extra {i}",
                hist="",
                cidade="São Paulo",
                uf="SP",
            )

        url = reverse("registry:loja_list")
        resp = self.client.get(url, {"q": "paulista", "per_page": "25", "page": "1"})
        self.assertEqual(resp.status_code, 200)

        content = resp.content.decode("utf-8")
        self.assertIn("q=paulista", content)
        self.assertIn("per_page=25", content)
