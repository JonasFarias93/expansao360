from __future__ import annotations

from django.core.files.uploadedfile import SimpleUploadedFile
from execucao.models import Chamado
from execucao.services.execution_session import create_active_session

from ._base import WebAuthBaseTestCase, grant_cap


class TestChamadoExecucaoRenderEvidencias(WebAuthBaseTestCase):
    def test_get_execucao_com_evidencia_sem_descricao_entao_renderiza_200(self) -> None:
        chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            status=Chamado.Status.ABERTO,
            tipo=Chamado.Tipo.ENVIO,
        )

        create_active_session(chamado=chamado, user=self.user)

        chamado.evidencias.create(
            tipo="CARTA_CONTEUDO",
            descricao="",
            nome_arquivo="nf_saida.pdf",
            arquivo=SimpleUploadedFile(
                "nf_saida.pdf",
                b"%PDF-1.4 dummy",
                content_type="application/pdf",
            ),
        )

        grant_cap(self.user, "execucao.chamado.visualizar")

        resp = self.client.get(f"/execucao/chamados/{chamado.id}/", follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "nf_saida.pdf")
