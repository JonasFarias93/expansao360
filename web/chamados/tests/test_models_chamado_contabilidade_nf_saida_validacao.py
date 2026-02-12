from django.core.exceptions import ValidationError
from execucao.models import NF_SAIDA_ONLY_DIGITS_ERROR, Chamado
from execucao.tests._base import ChamadoBaseTestCase


class ChamadoContabilidadeNFSaidaValidacaoTests(ChamadoBaseTestCase):
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

    def test_contabilidade_numero_trim(self) -> None:
        self.chamado.contabilidade_numero = "  PED-001  "
        self.chamado.full_clean()
        self.assertEqual(self.chamado.contabilidade_numero, "PED-001")

    def test_nf_saida_remove_espacos(self) -> None:
        self.chamado.nf_saida_numero = " 123 45 "
        self.chamado.full_clean()
        self.assertEqual(self.chamado.nf_saida_numero, "12345")

    def test_nf_saida_rejeita_nao_digitos(self) -> None:
        self.chamado.nf_saida_numero = "NF-123"
        with self.assertRaises(ValidationError) as ctx:
            self.chamado.full_clean()

        self.assertEqual(
            ctx.exception.message_dict["nf_saida_numero"],
            [NF_SAIDA_ONLY_DIGITS_ERROR],
        )
