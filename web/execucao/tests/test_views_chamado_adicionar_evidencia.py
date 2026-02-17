from __future__ import annotations
from execucao.services.execution_session import create_active_session
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from execucao.models import Chamado
from django.test import Client, RequestFactory
from django.middleware.csrf import get_token
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

    def test_quando_salva_execucao_entao_posso_anexar_evidencia_com_sessao_ativa(
        self,
    ) -> None:
        chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            status=Chamado.Status.ABERTO,
            tipo=Chamado.Tipo.ENVIO,
        )

        create_active_session(chamado=chamado, user=self.user)

        url_salvar = reverse(
            "execucao:chamado_salvar_execucao_ajax", kwargs={"chamado_id": chamado.id}
        )
        resp1 = self.client.post(
            url_salvar,
            data={"contabilidade_numero": "", "nf_saida_numero": ""},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(resp1.status_code, 200)

        url_evid = reverse("execucao:chamado_adicionar_evidencia", args=[chamado.id])

        arquivo = SimpleUploadedFile(
            "carta.pdf",
            b"%PDF-1.4 dummy",
            content_type="application/pdf",
        )

        before = chamado.evidencias.count()

        resp2 = self.client.post(
            url_evid,
            data={
                "tipo": "CARTA_CONTEUDO",
                "descricao": "Carta assinada",
                "arquivo": arquivo,
            },
        )

        self.assertEqual(resp2.status_code, 302)

        chamado.refresh_from_db()
        self.assertEqual(chamado.evidencias.count(), before + 1)


class TestChamadoAdicionarEvidenciaNomeArquivo(WebAuthBaseTestCase):
    def test_quando_anexa_evidencia_entao_persiste_nome_arquivo(self) -> None:
        chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
        )

        url_post = reverse("execucao:chamado_adicionar_evidencia", args=[chamado.id])

        client = Client(enforce_csrf_checks=True)
        client.force_login(self.user)

        rf = RequestFactory()
        req = rf.get("/")
        csrf_token = get_token(req)
        client.cookies["csrftoken"] = csrf_token

        upload = SimpleUploadedFile(
            "nf_saida.pdf",
            b"%PDF-1.4 dummy",
            content_type="application/pdf",
        )

        resp = client.post(
            url_post,
            data={
                "csrfmiddlewaretoken": csrf_token,
                "tipo": "CARTA_CONTEUDO",
                "descricao": "",
                "arquivo": upload,
            },
            HTTP_X_CSRFTOKEN=csrf_token,
        )

        self.assertEqual(resp.status_code, 302)

        chamado.refresh_from_db()
        self.assertEqual(chamado.evidencias.count(), 1)
        evidencia = chamado.evidencias.first()
        assert evidencia is not None

        self.assertEqual(evidencia.nome_arquivo, "nf_saida.pdf")
