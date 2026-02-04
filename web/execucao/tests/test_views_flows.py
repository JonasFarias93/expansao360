from __future__ import annotations

from cadastro.models import Equipamento
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from execucao.models import Chamado, InstalacaoItem

from ._base import WebAuthBaseTestCase


class ChamadoStatusFlowWebTest(WebAuthBaseTestCase):
    def test_post_atualizar_itens_muda_status_para_em_execucao(self) -> None:
        equipamento = Equipamento.objects.create(
            codigo="CABO",
            nome="Cabo",
            categoria=self.categoria,
            tem_ativo=False,
        )

        chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            status=Chamado.Status.ABERTO,
        )

        item = InstalacaoItem.objects.create(
            chamado=chamado,
            equipamento=equipamento,
            tipo="USB",
            quantidade=1,
            tem_ativo=False,
            confirmado=False,
        )

        url = reverse("execucao:chamado_atualizar_itens", args=[chamado.id])
        resp = self.client.post(url, {f"confirmado_{item.id}": "on"})

        self.assertEqual(resp.status_code, 302)

        chamado.refresh_from_db()
        item.refresh_from_db()

        self.assertEqual(chamado.status, Chamado.Status.EM_EXECUCAO)
        self.assertTrue(item.confirmado)


class EvidenciaChamadoWebTest(WebAuthBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
        )

    def test_post_adicionar_evidencia_cria_registro(self) -> None:
        url = reverse("execucao:chamado_adicionar_evidencia", args=[self.chamado.id])

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

        self.chamado.refresh_from_db()
        self.assertEqual(self.chamado.evidencias.count(), 1)
        evidencia = self.chamado.evidencias.first()
        assert evidencia is not None
        self.assertEqual(evidencia.tipo, "CARTA_CONTEUDO")
