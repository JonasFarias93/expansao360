from django.urls import reverse
from execucao.tests._base import WebAuthBaseTestCase, grant_cap

from cadastro.models import Loja


class LojaListBuscaTests(WebAuthBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        grant_cap(self.user, "cadastro.visualizar")

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

    def test_q_vazio_retorna_lista_padrao(self) -> None:
        url = reverse("registry:loja_list")

        resp_sem_q = self.client.get(url, {"per_page": "25"})
        self.assertEqual(resp_sem_q.status_code, 200)
        content_sem_q = resp_sem_q.content.decode("utf-8")

        resp_q_vazio = self.client.get(url, {"q": "   ", "per_page": "25"})
        self.assertEqual(resp_q_vazio.status_code, 200)
        content_q_vazio = resp_q_vazio.content.decode("utf-8")

        # garante que ambos mostram as lojas padrão
        for nome in ["Loja Paulista", "Loja Centro", "Loja Rio"]:
            self.assertIn(nome, content_sem_q)
            self.assertIn(nome, content_q_vazio)

    def test_q_numerico_bate_em_java_ou_hist(self) -> None:
        Loja.objects.create(codigo="6", nome="Loja Seis", hist="6", cidade="São Paulo", uf="SP")

        url = reverse("registry:loja_list")
        resp = self.client.get(url, {"q": "6", "per_page": "25"})
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode("utf-8")

        self.assertIn("Loja Seis", content)
        # as outras não deveriam aparecer nesse filtro numérico (iexact)
        self.assertNotIn("Loja Paulista", content)
        self.assertNotIn("Loja Centro", content)
        self.assertNotIn("Loja Rio", content)

    def test_q_texto_busca_por_nome(self) -> None:
        Loja.objects.create(codigo="10", nome="PAULISTA", hist="", cidade="Sao Paulo", uf="SP")

        url = reverse("registry:loja_list")
        resp = self.client.get(url, {"q": "PAULISTA", "per_page": "25"})
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode("utf-8")

        self.assertIn("PAULISTA", content)

    def test_pagina_2_com_filtro_funciona(self) -> None:
        # cria bastante coisa que bate por nome (texto)
        for i in range(30):
            Loja.objects.create(
                codigo=f"9{i}",
                nome=f"PAULISTA EXTRA {i}",
                hist="",
                cidade="São Paulo",
                uf="SP",
            )

        url = reverse("registry:loja_list")
        resp = self.client.get(url, {"q": "PAULISTA", "per_page": "10", "page": "2"})
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode("utf-8")

        # paginação preserva filtro e per_page nos links
        self.assertIn("q=PAULISTA", content)
        self.assertIn("per_page=10", content)

        # sanity check: página 2 deve ter itens
        self.assertIn("PAULISTA EXTRA", content)
