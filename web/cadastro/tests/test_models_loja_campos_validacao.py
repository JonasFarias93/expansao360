from django.core.exceptions import ValidationError
from django.test import TestCase

from cadastro.models import Loja


class TestLojaCamposValidacao(TestCase):
    def test_quando_cria_loja_entao_normaliza_uf_e_campos(self) -> None:
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

    def test_quando_uf_invalida_entao_full_clean_lanca_validation_error(self) -> None:
        loja = Loja(
            codigo="7",
            nome="SAO CARLOS - A",
            uf="SPO",
        )

        with self.assertRaises(ValidationError):
            loja.full_clean()
