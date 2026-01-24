from __future__ import annotations

from cadastro.models import Categoria, Equipamento, ItemKit, Kit, Loja, Projeto, Subprojeto
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from iam.models import Capability, UserCapability

from .models import Chamado, EvidenciaChamado, InstalacaoItem


def grant_cap(user, code: str) -> None:
    cap, _ = Capability.objects.get_or_create(code=code)
    UserCapability.objects.get_or_create(user=user, capability=cap)


class ChamadoBaseTestCase(TestCase):
    """Setup comum para cenários de execução."""

    def setUp(self) -> None:
        self.categoria = Categoria.objects.create(nome="Infra")
        self.loja = Loja.objects.create(codigo="L1", nome="Loja 1")
        self.projeto = Projeto.objects.create(codigo="P1", nome="Projeto 1")
        self.sub = Subprojeto.objects.create(
            projeto=self.projeto,
            codigo="S1",
            nome="Sub 1",
        )
        self.kit = Kit.objects.create(nome="Kit PDV")


class WebAuthBaseTestCase(ChamadoBaseTestCase):
    """Base para testes web (client autenticado + capabilities)."""

    def setUp(self) -> None:
        super().setUp()
        User = get_user_model()
        self.user = User.objects.create_user(username="u1", password="x")
        self.client.force_login(self.user)

        # Capabilities necessárias para os endpoints que são POST e sensíveis.
        # Ajuste aqui se você tiver separado por ação (ex.: upload vs editar_itens).
        grant_cap(self.user, "execucao.chamado.editar_itens")
        grant_cap(self.user, "execucao.evidencia.upload")
        grant_cap(self.user, "execucao.evidencia.remover")
        grant_cap(self.user, "execucao.item_configuracao.alterar_status")
        grant_cap(self.user, "execucao.chamado.finalizar")


class ChamadoGeracaoItensTest(ChamadoBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.micro = Equipamento.objects.create(
            codigo="MICRO",
            nome="Micro",
            categoria=self.categoria,
            tem_ativo=True,
        )
        self.hub = Equipamento.objects.create(
            codigo="HUB_USB",
            nome="Hub USB",
            categoria=self.categoria,
            tem_ativo=False,
        )

        ItemKit.objects.create(
            kit=self.kit,
            equipamento=self.micro,
            tipo="PDV",
            quantidade=1,
        )
        ItemKit.objects.create(
            kit=self.kit,
            equipamento=self.hub,
            tipo="USB",
            quantidade=2,
        )

    def test_criar_chamado_gera_itens_de_instalacao(self) -> None:
        chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
        )
        chamado.gerar_itens_de_instalacao()

        itens = InstalacaoItem.objects.filter(chamado=chamado).order_by("id")
        self.assertEqual(itens.count(), 2)

        micro_item = itens.get(equipamento__codigo="MICRO")
        self.assertEqual(micro_item.quantidade, 1)
        self.assertTrue(micro_item.tem_ativo)

    def test_item_sem_ativo_usa_confirmado(self) -> None:
        chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
        )
        chamado.gerar_itens_de_instalacao()

        hub_item = InstalacaoItem.objects.get(
            chamado=chamado,
            equipamento__codigo="HUB_USB",
        )
        hub_item.confirmado = True
        hub_item.save()

        hub_item.refresh_from_db()
        self.assertTrue(hub_item.confirmado)


class ValidacaoExecucaoChamadoTest(ChamadoBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.micro = Equipamento.objects.create(
            codigo="MICRO",
            nome="Micro",
            categoria=self.categoria,
            tem_ativo=True,
        )
        self.hub = Equipamento.objects.create(
            codigo="HUB_USB",
            nome="Hub USB",
            categoria=self.categoria,
            tem_ativo=False,
        )

        self.chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
        )

        self.item_micro = InstalacaoItem.objects.create(
            chamado=self.chamado,
            equipamento=self.micro,
            tipo="PDV",
            quantidade=1,
            tem_ativo=True,
        )
        self.item_hub = InstalacaoItem.objects.create(
            chamado=self.chamado,
            equipamento=self.hub,
            tipo="USB",
            quantidade=2,
            tem_ativo=False,
        )

    def test_finalizar_falha_se_item_com_ativo_sem_dados(self) -> None:
        with self.assertRaises(ValidationError):
            self.chamado.finalizar()

    def test_finalizar_falha_se_item_contavel_nao_confirmado(self) -> None:
        self.item_micro.ativo = "ATV-123"
        self.item_micro.numero_serie = "SER-999"
        self.item_micro.save()

        with self.assertRaises(ValidationError):
            self.chamado.finalizar()

    def test_finalizar_sucesso_e_define_data(self) -> None:
        self.item_micro.ativo = "ATV-123"
        self.item_micro.numero_serie = "SER-999"
        self.item_micro.save()

        self.item_hub.confirmado = True
        self.item_hub.save()

        self.chamado.finalizar()
        self.chamado.refresh_from_db()

        self.assertEqual(self.chamado.status, Chamado.Status.FINALIZADO)
        self.assertIsNotNone(self.chamado.finalizado_em)
        self.assertLessEqual(self.chamado.finalizado_em, timezone.now())

    def test_finalizar_falha_se_ja_estiver_finalizado(self) -> None:
        self.item_micro.ativo = "ATV-123"
        self.item_micro.numero_serie = "SER-999"
        self.item_micro.save()

        self.item_hub.confirmado = True
        self.item_hub.save()

        self.chamado.finalizar()

        with self.assertRaises(ValidationError) as ctx:
            self.chamado.finalizar()

        self.assertIn("já está finalizado", str(ctx.exception).lower())


class ValidacaoExecucaoChamadoSemItensTest(ChamadoBaseTestCase):
    def test_finalizar_falha_sem_itens(self) -> None:
        chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
        )

        with self.assertRaises(ValidationError) as ctx:
            chamado.finalizar()

        self.assertIn("sem itens", str(ctx.exception).lower())


class ChamadoProtocoloEReferenciasTest(ChamadoBaseTestCase):
    def test_protocolo_e_gerado_automaticamente(self) -> None:
        chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
        )
        self.assertTrue(chamado.protocolo)
        self.assertTrue(chamado.protocolo.startswith("EX360-"))

    def test_servicenow_numero_nao_repete(self) -> None:
        Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            servicenow_numero="SN-1002",
        )

        with self.assertRaises(IntegrityError):
            Chamado.objects.create(
                loja=self.loja,
                projeto=self.projeto,
                subprojeto=self.sub,
                kit=self.kit,
                servicenow_numero="SN-1002",
            )


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
