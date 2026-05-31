# web/chamados/tests/test_views_chamado_selecao.py
from __future__ import annotations

from django.urls import reverse
from chamados.tests._base import WebAuthBaseTestCase
from iam.models import Capability, UserCapability


class TestChamadoSelecaoView(WebAuthBaseTestCase):

    def setUp(self):
        super().setUp()
        for code in ["execucao.chamado.criar", "execucao.chamado.visualizar"]:
            cap, _ = Capability.objects.get_or_create(code=code)
            UserCapability.objects.get_or_create(user=self.user, capability=cap)

    def test_get_retorna_200(self):
        url = reverse("execucao:chamado_selecao")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_template_tem_link_projeto(self):
        url = reverse("execucao:chamado_selecao")
        resp = self.client.get(url)
        self.assertContains(resp, reverse("execucao:chamado_create_projeto"))

    def test_template_tem_link_avulso(self):
        url = reverse("execucao:chamado_selecao")
        resp = self.client.get(url)
        self.assertContains(resp, reverse("execucao:chamado_create_avulso"))