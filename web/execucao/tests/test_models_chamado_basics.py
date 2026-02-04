from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import IntegrityError

from execucao.models import Chamado

from ._base import ChamadoBaseTestCase


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
