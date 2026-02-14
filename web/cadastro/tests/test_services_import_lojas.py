from io import StringIO
from pathlib import Path
import tempfile

from django.core.management import call_command
from django.test import TestCase

from cadastro.models import Loja
from cadastro.services.import_lojas import importar_lojas, normalizar_loja_row

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
#  Import  / Lojas
# ==========================


class ImportLojasServiceTest(TestCase):
    def test_importar_lojas_idempotente(self) -> None:
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
