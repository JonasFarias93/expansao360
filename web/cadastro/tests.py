# Create your tests here.
from io import StringIO

from django.core.exceptions import ValidationError
from django.core.management import call_command
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
            "Logomarca": "raia",
            "Telefone": "11999990000",
            "IP Banco 12": "10.0.0.1",
        }

        out = normalizar_loja_row(row)

        self.assertEqual(out["codigo"], "123")
        self.assertEqual(out["hist"], "H1")
        self.assertEqual(out["nome"], "Loja Centro")
        self.assertEqual(out["endereco"], "Rua X, 10")
        self.assertEqual(out["bairro"], "Centro")
        self.assertEqual(out["cidade"], "São Paulo")
        self.assertEqual(out["uf"], "SP")
        self.assertEqual(out["logomarca"], "RAIA")
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


# ==========================
#  Form /cadasto / Loja
# ==========================


class LojaFormTest(TestCase):
    def test_loja_form_labels(self) -> None:
        from cadastro.forms import LojaForm

        form = LojaForm()
        self.assertEqual(form.fields["codigo"].label, "Java")
        self.assertEqual(form.fields["nome"].label, "Nome loja")
        self.assertIn("ip_banco_12", form.fields)


# ==========================
#  Import  / Lojas
# ==========================


class ImportLojasServiceTest(TestCase):
    def test_importar_lojas_idempotente(self) -> None:
        from cadastro.models import Loja
        from cadastro.services.import_lojas import importar_lojas

        rows = [
            {
                "Filial": "6",
                "Hist.": "6",
                "Nome Filial": "PAULISTA",
                "Endereço": "AV PAULISTA, 807",
                "Bairro": "BELA VISTA",
                "Cidade": "SAO PAULO",
                "UF": "sp",
                "Logomarca": "raia",
                "Telefone": "(11) 31710248",
                "IP Banco 12": "10.140.6.12",
            }
        ]

        r1 = importar_lojas(rows)
        self.assertEqual(r1["created"], 1)
        self.assertEqual(Loja.objects.count(), 1)

        # segunda rodada: não cria, não altera
        r2 = importar_lojas(rows)
        self.assertEqual(r2["created"], 0)
        self.assertEqual(r2["updated"], 0)
        self.assertEqual(r2["unchanged"], 1)
        self.assertEqual(Loja.objects.count(), 1)

        # altera um campo: deve atualizar
        rows2 = [dict(rows[0])]
        rows2[0]["Telefone"] = "(11) 00000000"
        r3 = importar_lojas(rows2)
        self.assertEqual(r3["updated"], 1)

        loja = Loja.objects.get(codigo="6")
        self.assertEqual(loja.telefone, "(11) 00000000")


class ImportLojasCommandTest(TestCase):
    def test_command_import_lojas_csv(self) -> None:
        from pathlib import Path
        import tempfile

        csv_content = (
            "Filial;Hist.;Nome Filial;Endereço;Bairro;Cidade;UF;Logomarca;Telefone;IP Banco 12\n"
            "6;6;PAULISTA;AV PAULISTA, 807;BELA VISTA;SAO PAULO;SP;RAIA;(11) 31710248;10.140.6.12\n"
        )

        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "lojas.csv"
            p.write_text(csv_content, encoding="utf-8")

            out = StringIO()
            call_command("import_lojas", str(p), stdout=out)

            s = out.getvalue()
            self.assertIn("Import concluído:", s)
            self.assertIn("Novas lojas: 1", s)
