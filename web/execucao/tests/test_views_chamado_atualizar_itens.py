from __future__ import annotations

from cadastro.models import Equipamento
from django.urls import reverse
from execucao.models import Chamado, InstalacaoItem

from ._base import WebAuthBaseTestCase


class TestChamadoAtualizarItensPostView(WebAuthBaseTestCase):
    def test_quando_confirma_item_entao_marca_confirmado_e_promove_para_em_execucao(
        self,
    ) -> None:
        equipamento = Equipamento.objects.create(
            codigo="CABO",
            nome="Cabo",
            categoria=self.categoria,
            tem_ativo=False,
        )

        chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            status=Chamado.Status.ABERTO,
        )

        item = InstalacaoItem.objects.create(
            chamado=chamado,
            equipamento=equipamento,
            tipo="USB",
            quantidade=1,
            tem_ativo=False,
            confirmado=False,
        )

        url = reverse("execucao:chamado_atualizar_itens", args=[chamado.id])
        resp = self.client.post(url, {f"confirmado_{item.id}": "on"})

        self.assertEqual(resp.status_code, 302)

        chamado.refresh_from_db()
        item.refresh_from_db()

        self.assertEqual(chamado.status, Chamado.Status.EM_EXECUCAO)
        self.assertTrue(item.confirmado)
