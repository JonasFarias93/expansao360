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

        tipo_pdv = TipoEquipamento.objects.create(
            categoria=self.categoria,
            codigo="PDV",
            nome="PDV",
        )

        ItemKit.objects.create(
            kit=kit,
            equipamento=self.equip_micro,
            tipo=tipo_pdv,
            quantidade=1,
        )

        with self.assertRaises(IntegrityError):
            ItemKit.objects.create(
                kit=kit,
                equipamento=self.equip_micro,
                tipo=tipo_pdv,
                quantidade=2,
            )

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
    def test_codigo_gerado_automaticamente_quando_vazio(self) -> None:
        cat = Categoria.objects.create(nome="Monitores")
        t = TipoEquipamento.objects.create(categoria=cat, nome="Touch")
        self.assertEqual(t.codigo, "TOUCH")

    def test_codigo_sufixa_quando_colisao_na_mesma_categoria(self) -> None:
        cat = Categoria.objects.create(nome="Monitores")
        t1 = TipoEquipamento.objects.create(categoria=cat, nome="LCD")
        t2 = TipoEquipamento.objects.create(categoria=cat, nome="LCD")
        self.assertEqual(t1.codigo, "LCD")
        self.assertEqual(t2.codigo, "LCD_2")

    def test_mesmo_nome_em_categorias_diferentes_pode_repetir_codigo(self) -> None:
        c1 = Categoria.objects.create(nome="Monitores")
        c2 = Categoria.objects.create(nome="Microcomputadores")

        t1 = TipoEquipamento.objects.create(categoria=c1, nome="PDV")
        t2 = TipoEquipamento.objects.create(categoria=c2, nome="PDV")

        self.assertEqual(t1.codigo, "PDV")
        self.assertEqual(t2.codigo, "PDV")

    def test_str_mostra_nome_e_codigo(self) -> None:
        cat = Categoria.objects.create(nome="Monitores")
        t = TipoEquipamento.objects.create(categoria=cat, nome="Touch")
        self.assertIn("Touch", str(t))
        self.assertIn("TOUCH", str(t))
