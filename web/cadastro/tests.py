# Create your tests here.
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from cadastro.services.import_lojas import normalizar_loja_row

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


# ==========================
# Import / Normalização Loja
# ==========================


class LojaImportMapperTest(TestCase):
    def test_normalizar_loja_row_mapeia_campos(self) -> None:
        row = {
            "Filial": " 123 ",
            "Hist.": "H1",
            "Nome Filial": " Loja Centro ",
            "Endereço": "Rua X, 10",
            "Bairro": "Centro",
            "Cidade": "São Paulo",
            "UF": "sp",
            "Logomarca": "logo.png",
            "Telefone": "11999990000",
            "IP Banco 12": "10.0.0.1",
        }

        out = normalizar_loja_row(row)

        self.assertEqual(out["filial"], "123")
        self.assertEqual(out["hist"], "H1")
        self.assertEqual(out["nome_loja"], "Loja Centro")
        self.assertEqual(out["endereco"], "Rua X, 10")
        self.assertEqual(out["bairro"], "Centro")
        self.assertEqual(out["cidade"], "São Paulo")
        self.assertEqual(out["uf"], "SP")  # normaliza UF
        self.assertEqual(out["logomarca"], "logo.png")
        self.assertEqual(out["telefone"], "11999990000")
        self.assertEqual(out["ip_banco_12"], "10.0.0.1")

    def test_normalizar_loja_row_ip_vazio_vira_none(self) -> None:
        row = {
            "Filial": "123",
            "Hist.": "",
            "Nome Filial": "Loja",
            "Endereço": "",
            "Bairro": "",
            "Cidade": "",
            "UF": "RJ",
            "Logomarca": "",
            "Telefone": "",
            "IP Banco 12": "   ",
        }

        out = normalizar_loja_row(row)
        self.assertIsNone(out["ip_banco_12"])


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
