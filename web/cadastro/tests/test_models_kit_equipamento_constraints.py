from django.db import IntegrityError
from django.test import TestCase

from cadastro.models import (
    Categoria,
    Equipamento,
    ItemKit,
    Kit,
    Projeto,
    Subprojeto,
    TipoEquipamento,
)


class TestKitEquipamentoConstraints(TestCase):
    def setUp(self) -> None:
        self.categoria = Categoria.objects.create(nome="Infra")
        self.equip_micro = Equipamento.objects.create(
            codigo="MICRO",
            nome="Micro",
            categoria=self.categoria,
            tem_ativo=True,
            configuravel=False,
        )
        self.equip_hub = Equipamento.objects.create(
            codigo="HUB_USB",
            nome="Hub USB",
            categoria=self.categoria,
            tem_ativo=False,
            configuravel=False,
        )

    def test_quando_equipamento_salvo_entao_tem_ativo_persistido(self) -> None:
        micro = Equipamento.objects.get(codigo="MICRO")
        hub = Equipamento.objects.get(codigo="HUB_USB")
        self.assertTrue(micro.tem_ativo)
        self.assertFalse(hub.tem_ativo)

    def test_quando_codigo_equipamento_duplicado_entao_integrity_error(self) -> None:
        with self.assertRaises(IntegrityError):
            Equipamento.objects.create(
                codigo="MICRO",
                nome="Micro duplicado",
                categoria=self.categoria,
                tem_ativo=True,
                configuravel=False,
            )

    def test_quando_itemkit_duplicado_no_mesmo_kit_tipo_entao_integrity_error(
        self,
    ) -> None:
        kit = Kit.objects.create(nome="Kit PDV")
        tipo = TipoEquipamento.objects.create(
            categoria=self.categoria,
            codigo="PDV",
            nome="PDV",
        )

        ItemKit.objects.create(
            kit=kit,
            equipamento=self.equip_micro,
            tipo=tipo,
            quantidade=1,
        )

        with self.assertRaises(IntegrityError):
            ItemKit.objects.create(
                kit=kit,
                equipamento=self.equip_micro,
                tipo=tipo,
                quantidade=2,
            )

    def test_quando_subprojeto_codigo_repetido_no_mesmo_projeto_entao_integrity_error(
        self,
    ) -> None:
        projeto = Projeto.objects.create(codigo="P1", nome="Projeto 1")
        Subprojeto.objects.create(projeto=projeto, codigo="S1", nome="Sub 1")

        with self.assertRaises(IntegrityError):
            Subprojeto.objects.create(
                projeto=projeto,
                codigo="S1",
                nome="Sub duplicado",
            )
