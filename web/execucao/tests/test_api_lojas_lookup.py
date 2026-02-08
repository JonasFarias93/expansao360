# web/execucao/tests/test_api_lojas_lookup.py
from __future__ import annotations

from cadastro.models import Loja
from django.test import TestCase
from django.urls import reverse


class LojaLookupPorCodigoApiTests(TestCase):
    def test_lookup_existente_retorna_payload_minimo(self) -> None:
        loja = Loja.objects.create(codigo="3500", nome="BROOKLIN NOVO")

        url = reverse("execucao:api_loja_lookup")
        resp = self.client.get(url, {"codigo": "3500"})

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            resp.json(),
            {"id": loja.id, "codigo": "3500", "nome": "BROOKLIN NOVO"},
        )

    def test_lookup_inexistente_retorna_404(self) -> None:
        url = reverse("execucao:api_loja_lookup")
        resp = self.client.get(url, {"codigo": "9999"})

        self.assertEqual(resp.status_code, 404)

    def test_lookup_invalido_retorna_400(self) -> None:
        url = reverse("execucao:api_loja_lookup")

        # vazio
        resp1 = self.client.get(url, {"codigo": ""})
        self.assertEqual(resp1.status_code, 400)

        # não numérico
        resp2 = self.client.get(url, {"codigo": "35A0"})
        self.assertEqual(resp2.status_code, 400)

        # ausente
        resp3 = self.client.get(url)
        self.assertEqual(resp3.status_code, 400)
