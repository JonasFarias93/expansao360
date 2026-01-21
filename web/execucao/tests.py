# Create your tests here.
from cadastro.models import Categoria, Equipamento, ItemKit, Kit, Loja, Projeto, Subprojeto
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from .models import Chamado, InstalacaoItem


class ChamadoGeracaoItensTest(TestCase):
    def setUp(self) -> None:
        self.categoria = Categoria.objects.create(nome="Infra")

        self.micro = Equipamento.objects.create(
            codigo="MICRO",
            nome="Micro",
            categoria=self.categoria,
            tem_ativo=True,
            configuravel=False,
        )
        self.hub = Equipamento.objects.create(
            codigo="HUB_USB",
            nome="Hub USB",
            categoria=self.categoria,
            tem_ativo=False,
            configuravel=False,
        )

        self.kit = Kit.objects.create(nome="Kit PDV")
        ItemKit.objects.create(kit=self.kit, equipamento=self.micro, tipo="PDV", quantidade=1)
        ItemKit.objects.create(kit=self.kit, equipamento=self.hub, tipo="USB", quantidade=2)

        self.loja = Loja.objects.create(codigo="L1", nome="Loja 1")
        self.projeto = Projeto.objects.create(codigo="P1", nome="Projeto 1")
        self.sub = Subprojeto.objects.create(projeto=self.projeto, codigo="S1", nome="Sub 1")

    def test_criar_chamado_gera_itens_de_instalacao(self) -> None:
        chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
        )

        # ação (ainda não existe): gerar itens
        chamado.gerar_itens_de_instalacao()

        itens = InstalacaoItem.objects.filter(chamado=chamado).order_by("id")
        self.assertEqual(itens.count(), 2)

        micro_item = itens[0]
        self.assertEqual(micro_item.equipamento.codigo, "MICRO")
        self.assertEqual(micro_item.tipo, "PDV")
        self.assertEqual(micro_item.quantidade, 1)
        self.assertTrue(micro_item.tem_ativo)

        hub_item = itens[1]
        self.assertEqual(hub_item.equipamento.codigo, "HUB_USB")
        self.assertEqual(hub_item.tipo, "USB")
        self.assertEqual(hub_item.quantidade, 2)
        self.assertFalse(hub_item.tem_ativo)

    def test_item_sem_ativo_usa_confirmado(self) -> None:
        chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
        )
        chamado.gerar_itens_de_instalacao()

        hub_item = InstalacaoItem.objects.get(chamado=chamado, equipamento__codigo="HUB_USB")
        self.assertFalse(hub_item.tem_ativo)
        self.assertFalse(hub_item.confirmado)  # padrão
        hub_item.confirmado = True
        hub_item.save()

        hub_item.refresh_from_db()
        self.assertTrue(hub_item.confirmado)


class ValidacaoExecucaoChamadoTest(TestCase):
    def setUp(self) -> None:
        self.categoria = Categoria.objects.create(nome="Infra")

        self.micro = Equipamento.objects.create(
            codigo="MICRO",
            nome="Micro",
            categoria=self.categoria,
            tem_ativo=True,
            configuravel=False,
        )
        self.hub = Equipamento.objects.create(
            codigo="HUB_USB",
            nome="Hub USB",
            categoria=self.categoria,
            tem_ativo=False,
            configuravel=False,
        )

        self.kit = Kit.objects.create(nome="Kit PDV")
        ItemKit.objects.create(kit=self.kit, equipamento=self.micro, tipo="PDV", quantidade=1)
        ItemKit.objects.create(kit=self.kit, equipamento=self.hub, tipo="USB", quantidade=2)

        self.loja = Loja.objects.create(codigo="L1", nome="Loja 1")
        self.projeto = Projeto.objects.create(codigo="P1", nome="Projeto 1")
        self.sub = Subprojeto.objects.create(projeto=self.projeto, codigo="S1", nome="Sub 1")

        self.chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
        )
        self.chamado.gerar_itens_de_instalacao()

    def test_finalizar_falha_se_item_com_ativo_sem_dados(self) -> None:
        # Micro tem_ativo=True mas está sem ativo e série
        with self.assertRaises(ValidationError):
            self.chamado.finalizar()

    def test_finalizar_falha_se_item_contavel_nao_confirmado(self) -> None:
        # Preenche o Micro corretamente, mas Hub continua não confirmado
        micro_item = InstalacaoItem.objects.get(chamado=self.chamado, equipamento__codigo="MICRO")
        micro_item.ativo = "ATV-123"
        micro_item.numero_serie = "SER-999"
        micro_item.save()

        with self.assertRaises(ValidationError):
            self.chamado.finalizar()

    def test_finalizar_ok_quando_tudo_valido(self) -> None:
        micro_item = InstalacaoItem.objects.get(chamado=self.chamado, equipamento__codigo="MICRO")
        micro_item.ativo = "ATV-123"
        micro_item.numero_serie = "SER-999"
        micro_item.save()

        hub_item = InstalacaoItem.objects.get(chamado=self.chamado, equipamento__codigo="HUB_USB")
        hub_item.confirmado = True
        hub_item.save()

        # Agora deve finalizar sem erro
        self.chamado.finalizar()
        self.chamado.refresh_from_db()
        self.assertEqual(self.chamado.status, Chamado.Status.FINALIZADO)


def test_finalizar_define_finalizado_em(self) -> None:
    micro_item = InstalacaoItem.objects.get(chamado=self.chamado, equipamento__codigo="MICRO")
    micro_item.ativo = "ATV-123"
    micro_item.numero_serie = "SER-999"
    micro_item.save()

    hub_item = InstalacaoItem.objects.get(chamado=self.chamado, equipamento__codigo="HUB_USB")
    hub_item.confirmado = True
    hub_item.save()

    self.chamado.finalizar()
    self.chamado.refresh_from_db()
    self.assertIsNotNone(self.chamado.finalizado_em)
    self.assertLessEqual(self.chamado.finalizado_em, timezone.now())
