from __future__ import annotations

from django.core.files.uploadedfile import SimpleUploadedFile

from execucao.models import Chamado, EvidenciaChamado

from ._base import ChamadoBaseTestCase


class EvidenciaChamadoModelTest(ChamadoBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
        )

    def test_criar_evidencia_vinculada_ao_chamado(self) -> None:
        arquivo = SimpleUploadedFile(
            "nf_saida.pdf",
            b"%PDF-1.4 dummy",
            content_type="application/pdf",
        )

        evidencia = EvidenciaChamado.objects.create(
            chamado=self.chamado,
            tipo=EvidenciaChamado.Tipo.NF_SAIDA,
            arquivo=arquivo,
        )

        self.assertEqual(evidencia.chamado_id, self.chamado.id)
        self.assertTrue(evidencia.arquivo.name)
