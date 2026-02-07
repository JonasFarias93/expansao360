from __future__ import annotations

from django.db import IntegrityError

from execucao.models import Chamado

from ._base import ChamadoBaseTestCase


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

    def test_ticket_externo_nao_repete_por_sistema(self) -> None:
        Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            ticket_externo_sistema="ServiceNow",
            ticket_externo_id="SN-1002",
        )

        with self.assertRaises(IntegrityError):
            Chamado.objects.create(
                loja=self.loja,
                projeto=self.projeto,
                subprojeto=self.sub,
                kit=self.kit,
                ticket_externo_sistema="ServiceNow",
                ticket_externo_id="SN-1002",
            )

    def test_ticket_externo_pode_repetir_em_sistemas_diferentes(self) -> None:
        Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            ticket_externo_sistema="ServiceNow",
            ticket_externo_id="SN-1002",
        )

        # mesmo id, outro sistema => permitido
        Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            ticket_externo_sistema="Jira",
            ticket_externo_id="SN-1002",
        )
