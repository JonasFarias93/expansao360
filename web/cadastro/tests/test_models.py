from django.core.exceptions import ValidationError
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


# ==========================
# cadasto / Loja
# ==========================


class LojaModelCamposExtrasTest(TestCase):
    def test_loja_recebe_campos_extras_e_normaliza_uf(self) -> None:
        from cadastro.models import Loja

        loja = Loja.objects.create(
            codigo="6",
            nome="PAULISTA",
            hist="6",
            endereco="AVENIDA PAULISTA, 807",
            bairro="BELA VISTA",
            cidade="SAO PAULO",
            uf="sp",
            logomarca="RAIA",
            telefone="(11) 31710248          ",
            ip_banco_12="10.140.6.12",
        )

        loja.refresh_from_db()
        self.assertEqual(loja.uf, "SP")
        self.assertEqual(loja.ip_banco_12, "10.140.6.12")
        self.assertEqual(loja.telefone.strip(), "(11) 31710248")

    def test_loja_uf_invalida_quebra_no_clean(self) -> None:
        from cadastro.models import Loja

        loja = Loja(
            codigo="7",
            nome="SAO CARLOS - A",
            uf="SPO",
        )
        with self.assertRaises(ValidationError):
            loja.full_clean()


# ==========================
# cadasto / Tipo Equipamento
# ==========================


class TipoEquipamentoModelTest(TestCase):
    def test_tipo_equipamento_unico_por_categoria_codigo(self) -> None:
        cat = Categoria.objects.create(nome="Monitores")

        TipoEquipamento.objects.create(categoria=cat, codigo="LCD", nome="LCD")

        with self.assertRaises(IntegrityError):
            TipoEquipamento.objects.create(categoria=cat, codigo="LCD", nome="LCD duplicado")

    def test_tipo_equipamento_str(self) -> None:
        cat = Categoria.objects.create(nome="Monitores")
        t = TipoEquipamento.objects.create(categoria=cat, codigo="TOUCH", nome="Touch")
        self.assertIn("Touch", str(t))
