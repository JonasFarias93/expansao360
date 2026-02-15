from __future__ import annotations

from django.db import IntegrityError
from execucao.models import Chamado

from ._base import ChamadoBaseTestCase


class TestChamadoProtocoloETicketExternoConstraints(ChamadoBaseTestCase):
    def test_quando_cria_chamado_entao_protocolo_e_gerado_no_padrao(self) -> None:
        chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
        )
        self.assertTrue(chamado.protocolo)
        self.assertRegex(chamado.protocolo, r"^CHA-\d{6}$")

    def test_quando_cria_dois_chamados_entao_protocolo_e_unico_e_incrementa(
        self,
    ) -> None:
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

    def test_quando_salva_novamente_entao_protocolo_nao_muda(self) -> None:
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

    def test_quando_repite_ticket_externo_mesmo_sistema_entao_violacao_de_unicidade(
        self,
    ) -> None:
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

    def test_quando_repite_ticket_externo_em_sistemas_diferentes_entao_e_permitido(
        self,
    ) -> None:
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
