from __future__ import annotations

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from iam.models import Capability, UserCapability

from cadastro.models import Categoria, Equipamento, ItemKit, Kit, TipoEquipamento


class KitItensEndpointTests(TestCase):
    def setUp(self) -> None:
        User = get_user_model()
        self.user = User.objects.create_user(username="u", password="pw")
        self.client.force_login(self.user)

        cap = Capability.objects.create(code="cadastro.visualizar")
        UserCapability.objects.create(user=self.user, capability=cap)

        self.kit = Kit.objects.create(nome="Kit A")
        self.categoria = Categoria.objects.create(nome="Impressoras")
        self.equip = Equipamento.objects.create(nome="Impressora", categoria=self.categoria)
        self.tipo = TipoEquipamento.objects.create(
            nome="Térmica",
            categoria=self.categoria,
            disponivel=True,
        )

    def test_endpoint_retorna_itens(self) -> None:
        ItemKit.objects.create(
            kit=self.kit,
            equipamento=self.equip,
            tipo=self.tipo,
            quantidade=2,
            requer_configuracao=True,
        )

        url = reverse("registry:api_kit_itens", args=[self.kit.id])
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        data = resp.json()

        self.assertEqual(data["kit"]["nome"], "Kit A")
        self.assertEqual(len(data["itens"]), 1)
        self.assertEqual(data["itens"][0]["nome"], "Impressora Térmica")
        self.assertEqual(data["itens"][0]["quantidade"], 2)
        self.assertTrue(data["itens"][0]["requer_configuracao"])

    def test_endpoint_retorna_vazio(self) -> None:
        url = reverse("registry:api_kit_itens", args=[self.kit.id])
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["itens"], [])

    def test_endpoint_404(self) -> None:
        url = reverse("registry:api_kit_itens", args=[99999])
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 404)

    def test_sem_capability_retorna_403(self) -> None:
        UserCapability.objects.all().delete()

        url = reverse("registry:api_kit_itens", args=[self.kit.id])
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 403)
