# Create your tests here.
from django.db import IntegrityError
from django.test import TestCase

from .models import Categoria, Equipamento, ItemKit, Kit, Projeto, Subprojeto


class CadastroModelsTest(TestCase):
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

    def test_equipamento_tem_ativo_persistido(self) -> None:
        micro = Equipamento.objects.get(codigo="MICRO")
        hub = Equipamento.objects.get(codigo="HUB_USB")
        self.assertTrue(micro.tem_ativo)
        self.assertFalse(hub.tem_ativo)

    def test_equipamento_codigo_unico(self) -> None:
        with self.assertRaises(IntegrityError):
            Equipamento.objects.create(
                codigo="MICRO",
                nome="Micro duplicado",
                categoria=self.categoria,
                tem_ativo=True,
                configuravel=False,
            )

    def test_itemkit_unico_por_kit_equipamento_tipo(self) -> None:
        kit = Kit.objects.create(nome="Kit PDV")
        ItemKit.objects.create(kit=kit, equipamento=self.equip_micro, tipo="PDV", quantidade=1)

        with self.assertRaises(IntegrityError):
            ItemKit.objects.create(kit=kit, equipamento=self.equip_micro, tipo="PDV", quantidade=2)

    def test_subprojeto_unico_por_projeto_codigo(self) -> None:
        projeto = Projeto.objects.create(codigo="P1", nome="Projeto 1")
        Subprojeto.objects.create(projeto=projeto, codigo="S1", nome="Sub 1")

        with self.assertRaises(IntegrityError):
            Subprojeto.objects.create(projeto=projeto, codigo="S1", nome="Sub duplicado")
