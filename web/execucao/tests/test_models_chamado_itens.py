from __future__ import annotations

from cadastro.models import Equipamento, ItemKit, TipoEquipamento

from execucao.models import Chamado, InstalacaoItem

from ._base import ChamadoBaseTestCase


class ChamadoGeracaoItensTest(ChamadoBaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.micro = Equipamento.objects.create(
            codigo="MICRO",
            nome="Micro",
            categoria=self.categoria,
            tem_ativo=True,
        )
        self.hub = Equipamento.objects.create(
            codigo="HUB_USB",
            nome="Hub USB",
            categoria=self.categoria,
            tem_ativo=False,
        )

        self.tipo_pdv = TipoEquipamento.objects.create(
            categoria=self.categoria,
            codigo="PDV",
            nome="PDV",
        )
        self.tipo_usb = TipoEquipamento.objects.create(
            categoria=self.categoria,
            codigo="USB",
            nome="USB",
        )

        ItemKit.objects.create(
            kit=self.kit,
            equipamento=self.micro,
            tipo=self.tipo_pdv,
            quantidade=1,
        )
        ItemKit.objects.create(
            kit=self.kit,
            equipamento=self.hub,
            tipo=self.tipo_usb,
            quantidade=2,
        )

    def test_criar_chamado_gera_itens_de_instalacao(self) -> None:
        chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
        )
        chamado.gerar_itens_de_instalacao()

        itens = InstalacaoItem.objects.filter(chamado=chamado).order_by("id")
        self.assertEqual(itens.count(), 2)

        micro_item = itens.get(equipamento__codigo="MICRO")
        self.assertEqual(micro_item.quantidade, 1)
        self.assertTrue(micro_item.tem_ativo)

    def test_item_sem_ativo_usa_confirmado(self) -> None:
        chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
        )
        chamado.gerar_itens_de_instalacao()

        hub_item = InstalacaoItem.objects.get(
            chamado=chamado,
            equipamento__codigo="HUB_USB",
        )
        hub_item.confirmado = True
        hub_item.save()

        hub_item.refresh_from_db()
        self.assertTrue(hub_item.confirmado)
