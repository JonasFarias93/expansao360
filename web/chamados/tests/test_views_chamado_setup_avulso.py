# web/chamados/tests/test_views_chamado_setup_avulso.py
from __future__ import annotations

from django.urls import reverse
from chamados.models import Chamado, InstalacaoItem
from chamados.tests._base import WebAuthBaseTestCase
from cadastro.models import Categoria, Equipamento, TipoEquipamento
from iam.models import Capability, UserCapability


class TestChamadoSetupAvulsoView(WebAuthBaseTestCase):

    def setUp(self):
        super().setUp()
        for code in ["execucao.chamado.criar", "execucao.chamado.visualizar", "execucao.chamado.editar_itens"]:
            cap, _ = Capability.objects.get_or_create(code=code)
            UserCapability.objects.get_or_create(user=self.user, capability=cap)

        self.categoria = Categoria.objects.get_or_create(nome="Infra")[0]
        self.tipo = TipoEquipamento.objects.create(categoria=self.categoria, nome="Padrão")
        self.equipamento = Equipamento.objects.create(
            nome="Monitor", categoria=self.categoria, tem_ativo=True
        )
        self.chamado = Chamado.objects.create(
            loja=self.loja,
            is_avulso=True,
            status=Chamado.Status.EM_ABERTURA,
        )

    def _url(self):
        return reverse("execucao:chamado_setup_avulso", args=[self.chamado.id])

    def test_get_retorna_200(self):
        resp = self.client.get(self._url())
        self.assertEqual(resp.status_code, 200)

    def test_post_adiciona_item_ao_chamado(self):
        self.client.post(self._url(), {
            "equipamento": self.equipamento.pk,
            "tipo": self.tipo.pk,
            "quantidade": 2,
        })
        # tem_ativo=True → explode em linhas unitárias (2 itens)
        self.assertEqual(InstalacaoItem.objects.filter(chamado=self.chamado).count(), 2)
        item = InstalacaoItem.objects.filter(chamado=self.chamado).first()
        self.assertEqual(item.quantidade, 1)

    def test_post_salvar_promove_para_aberto(self):
        self.client.post(self._url(), {
            "equipamento": self.equipamento.pk,
            "tipo": self.tipo.pk,
            "quantidade": 1,
        })
        self.client.post(self._url(), {"acao": "salvar"})
        self.chamado.refresh_from_db()
        self.assertEqual(self.chamado.status, Chamado.Status.ABERTO)