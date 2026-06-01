# web/chamados/tests/test_views_chamado_avulso.py
from __future__ import annotations

from django.urls import reverse
from chamados.models import Chamado
from chamados.tests._base import WebAuthBaseTestCase
from iam.models import Capability, UserCapability


class TestChamadoCreateAvulsoView(WebAuthBaseTestCase):

    def setUp(self):
        super().setUp()
        for code in ["execucao.chamado.criar", "execucao.chamado.visualizar"]:
            cap, _ = Capability.objects.get_or_create(code=code)
            UserCapability.objects.get_or_create(user=self.user, capability=cap)

    def _url(self):
        return reverse("execucao:chamado_create_avulso")

    def test_get_retorna_200(self):
        resp = self.client.get(self._url())
        self.assertEqual(resp.status_code, 200)

    def test_post_cria_chamado_avulso_sem_projeto(self):
        resp = self.client.post(self._url(), {
            "loja": self.loja.pk,
            "prioridade": Chamado.Prioridade.PADRAO,
        })
        self.assertEqual(Chamado.objects.filter(is_avulso=True).count(), 1)
        chamado = Chamado.objects.get(is_avulso=True)
        self.assertIsNone(chamado.projeto)
        self.assertIsNone(chamado.kit)
        self.assertEqual(chamado.status, Chamado.Status.EM_ABERTURA)

    def test_post_sem_loja_retorna_form_com_erro(self):
        resp = self.client.post(self._url(), {
            "prioridade": Chamado.Prioridade.PADRAO,
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Chamado.objects.filter(is_avulso=True).count(), 0)