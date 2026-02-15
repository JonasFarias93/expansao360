from __future__ import annotations

from django.core.exceptions import ValidationError
from execucao.models import NF_SAIDA_ONLY_DIGITS_ERROR, Chamado
from execucao.tests._base import ChamadoBaseTestCase


class TestChamadoFiscalFieldsCleanValidation(ChamadoBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            status=Chamado.Status.ABERTO,
            tipo=Chamado.Tipo.ENVIO,
        )

    def test_quando_full_clean_entao_contabilidade_numero_e_trimado(self) -> None:
        self.chamado.contabilidade_numero = "  PED-001  "

        self.chamado.full_clean()

        self.assertEqual(self.chamado.contabilidade_numero, "PED-001")

    def test_quando_full_clean_entao_nf_saida_remove_espacos(self) -> None:
        self.chamado.nf_saida_numero = " 123 45 "

        self.chamado.full_clean()

        self.assertEqual(self.chamado.nf_saida_numero, "12345")

    def test_quando_full_clean_e_nf_saida_tem_nao_digitos_entao_lanca_validation_error(
        self,
    ) -> None:
        self.chamado.nf_saida_numero = "NF-123"

        with self.assertRaises(ValidationError) as ctx:
            self.chamado.full_clean()

        self.assertEqual(
            ctx.exception.message_dict["nf_saida_numero"],
            [NF_SAIDA_ONLY_DIGITS_ERROR],
        )
