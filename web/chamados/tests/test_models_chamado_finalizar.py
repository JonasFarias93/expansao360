from __future__ import annotations

from cadastro.models import Equipamento
from django.core.exceptions import ValidationError
from django.utils import timezone
from execucao.models import Chamado, InstalacaoItem

from ._base import ChamadoBaseTestCase


class TestChamadoFinalizarModel(ChamadoBaseTestCase):
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
            # gates ENVIO (as-is do projeto)
            nf_saida_numero="NF-123",
            coleta_confirmada_em=timezone.now(),
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
        self.chamado.nf_saida_numero = "NF-123"
        self.chamado.coleta_confirmada_em = timezone.now()
        self.chamado.save(update_fields=["nf_saida_numero", "coleta_confirmada_em"])

    def _bipar_item_rastreavel(self) -> None:
        self.item_micro.ativo = "ATV-123"
        self.item_micro.numero_serie = "SER-999"
        self.item_micro.save(update_fields=["ativo", "numero_serie"])

    def _confirmar_item_contavel(self) -> None:
        self.item_hub.confirmado = True
        self.item_hub.save(update_fields=["confirmado"])

    def test_quando_item_rastreavel_sem_dados_entao_finalizar_lanca_validation_error(
        self,
    ) -> None:
        self._liberar_gates_envio()
        with self.assertRaises(ValidationError):
            self.chamado.finalizar()

    def test_quando_item_contavel_nao_confirmado_entao_finalizar_lanca_validation_error(
        self,
    ) -> None:
        self._liberar_gates_envio()
        self._bipar_item_rastreavel()

        with self.assertRaises(ValidationError):
            self.chamado.finalizar()

    def test_quando_itens_ok_entao_finalizar_muda_status_e_define_finalizado_em(
        self,
    ) -> None:
        self._liberar_gates_envio()
        self._bipar_item_rastreavel()
        self._confirmar_item_contavel()

        self.chamado.finalizar()
        self.chamado.refresh_from_db()

        self.assertEqual(self.chamado.status, Chamado.Status.FINALIZADO)
        self.assertIsNotNone(self.chamado.finalizado_em)
        self.assertLessEqual(self.chamado.finalizado_em, timezone.now())

    def test_quando_ja_finalizado_entao_finalizar_novamente_lanca_validation_error(
        self,
    ) -> None:
        self._liberar_gates_envio()
        self._bipar_item_rastreavel()
        self._confirmar_item_contavel()

        self.chamado.finalizar()

        with self.assertRaises(ValidationError) as ctx:
            self.chamado.finalizar()

        self.assertIn("já está finalizado", str(ctx.exception).lower())
