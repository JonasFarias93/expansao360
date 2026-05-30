from __future__ import annotations

from cadastro.models import Equipamento, ItemKit, TipoEquipamento
from execucao.models import Chamado, InstalacaoItem

from ._base import ChamadoBaseTestCase


class TestChamadoGerarItensDeInstalacao(ChamadoBaseTestCase):
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

    def test_quando_gera_itens_entao_cria_itens_do_kit_com_quantidade_e_tem_ativo(
        self,
    ) -> None:
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

    def test_quando_item_nao_tem_ativo_entao_confirmado_pode_ser_marcado(self) -> None:
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


    def test_quando_item_kit_requer_configuracao_entao_snapshot_deve_configurar_true(
        self,
    ) -> None:
        """
        requer_configuracao=True no Kit deve propagar deve_configurar=True no snapshot.
        """
        self.micro.configuravel = True
        self.micro.save(update_fields=["configuravel"])

        ItemKit.objects.filter(kit=self.kit, equipamento=self.micro).update(
            requer_configuracao=True
        )

        chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
        )
        chamado.gerar_itens_de_instalacao()

        item = InstalacaoItem.objects.get(chamado=chamado, equipamento=self.micro)
        self.assertTrue(item.deve_configurar)
        self.assertTrue(item.requer_configuracao)


    def test_quando_item_kit_nao_requer_configuracao_entao_deve_configurar_false(
        self,
    ) -> None:
        """
        requer_configuracao=False no Kit não deve setar deve_configurar=True.
        """
        chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
        )
        chamado.gerar_itens_de_instalacao()

        for item in InstalacaoItem.objects.filter(chamado=chamado):
            self.assertFalse(item.deve_configurar)