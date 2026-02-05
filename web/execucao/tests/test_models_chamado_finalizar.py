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

    def _liberar_gates_envio(self) -> None:
        """
        A partir da regra nova, Chamado ENVIO só finaliza se:
        - nf_saida_numero preenchido
        - coleta_confirmada_em preenchido
        """
        self.chamado.nf_saida_numero = "NF-123"
        self.chamado.coleta_confirmada_em = timezone.now()
        self.chamado.save(update_fields=["nf_saida_numero", "coleta_confirmada_em"])

    def test_finalizar_falha_se_item_com_ativo_sem_dados(self) -> None:
        self._liberar_gates_envio()
        with self.assertRaises(ValidationError):
            self.chamado.finalizar()

    def test_finalizar_falha_se_item_contavel_nao_confirmado(self) -> None:
        self._liberar_gates_envio()

        self.item_micro.ativo = "ATV-123"
        self.item_micro.numero_serie = "SER-999"
        self.item_micro.save(update_fields=["ativo", "numero_serie"])

        with self.assertRaises(ValidationError):
            self.chamado.finalizar()

    def test_finalizar_sucesso_e_define_data(self) -> None:
        self._liberar_gates_envio()

        self.item_micro.ativo = "ATV-123"
        self.item_micro.numero_serie = "SER-999"
        self.item_micro.save(update_fields=["ativo", "numero_serie"])

        self.item_hub.confirmado = True
        self.item_hub.save(update_fields=["confirmado"])

        self.chamado.finalizar()
        self.chamado.refresh_from_db()

        self.assertEqual(self.chamado.status, Chamado.Status.FINALIZADO)
        self.assertIsNotNone(self.chamado.finalizado_em)
        self.assertLessEqual(self.chamado.finalizado_em, timezone.now())

    def test_finalizar_falha_se_ja_estiver_finalizado(self) -> None:
        self._liberar_gates_envio()

        self.item_micro.ativo = "ATV-123"
        self.item_micro.numero_serie = "SER-999"
        self.item_micro.save(update_fields=["ativo", "numero_serie"])

        self.item_hub.confirmado = True
        self.item_hub.save(update_fields=["confirmado"])

        self.chamado.finalizar()

        with self.assertRaises(ValidationError) as ctx:
            self.chamado.finalizar()

        self.assertIn("já está finalizado", str(ctx.exception).lower())
