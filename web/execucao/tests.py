from cadastro.models import Categoria, Equipamento, ItemKit, Kit, Loja, Projeto, Subprojeto
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Chamado, InstalacaoItem


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


class ChamadoStatusFlowWebTest(ChamadoBaseTestCase):
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
