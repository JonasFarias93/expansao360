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
        self.assertRegex(chamado.protocolo, r"^CHA-\d{6}$")

    def test_protocolo_e_unico_e_incremental(self) -> None:
        c1 = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
        )
        c2 = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
        )

        self.assertNotEqual(c1.protocolo, c2.protocolo)

        n1 = int(c1.protocolo.split("-", 1)[1])
        n2 = int(c2.protocolo.split("-", 1)[1])
        self.assertGreater(n2, n1)

    def test_protocolo_nao_muda_em_save_posterior(self) -> None:
        chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
        )
        original = chamado.protocolo

        # simula um "save" posterior (alterando qualquer campo mutável)
        chamado.save()
        chamado.refresh_from_db()
        self.assertEqual(chamado.protocolo, original)

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
