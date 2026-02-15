from __future__ import annotations

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from execucao.models import Chamado

from ._base import WebAuthBaseTestCase


class TestChamadoAdicionarEvidenciaPostView(WebAuthBaseTestCase):
    def test_quando_envia_pdf_entao_cria_evidencia_com_tipo_e_descricao(self) -> None:
        chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
        )

        url = reverse("execucao:chamado_adicionar_evidencia", args=[chamado.id])

        arquivo = SimpleUploadedFile(
            "carta.pdf",
            b"%PDF-1.4 dummy",
            content_type="application/pdf",
        )

        resp = self.client.post(
            url,
            data={
                "tipo": "CARTA_CONTEUDO",
                "descricao": "Carta assinada",
                "arquivo": arquivo,
            },
        )

        self.assertEqual(resp.status_code, 302)

        chamado.refresh_from_db()
        self.assertEqual(chamado.evidencias.count(), 1)

        evidencia = chamado.evidencias.first()
        assert evidencia is not None
        self.assertEqual(evidencia.tipo, "CARTA_CONTEUDO")
        self.assertEqual(evidencia.descricao, "Carta assinada")
