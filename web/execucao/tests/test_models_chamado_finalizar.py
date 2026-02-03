from __future__ import annotations

from cadastro.models import Equipamento
from django.core.exceptions import ValidationError
from django.utils import timezone

from execucao.models import Chamado, InstalacaoItem

from ._base import ChamadoBaseTestCase


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
