# web/chamados/tests/test_services_cancelamento.py
from __future__ import annotations

from django.core.exceptions import ValidationError

from chamados.models import Chamado
from chamados.services.cancelamento import cancelar_chamado
from chamados.tests._base import WebAuthBaseTestCase


class TestCancelarChamado(WebAuthBaseTestCase):

    def _chamado(self, status):
        c = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            status=status,
        )
        return c

    def test_cancela_chamado_aberto_com_motivo(self):
        c = self._chamado(Chamado.Status.ABERTO)
        cancelar_chamado(c, self.user, "Pedido cancelado pelo cliente.")
        c.refresh_from_db()
        self.assertEqual(c.status, Chamado.Status.CANCELADO)
        self.assertIsNotNone(c.cancelado_em)
        self.assertEqual(c.cancelado_por, self.user)
        self.assertEqual(c.motivo_cancelamento, "Pedido cancelado pelo cliente.")

    def test_cancela_em_abertura(self):
        c = self._chamado(Chamado.Status.EM_ABERTURA)
        cancelar_chamado(c, self.user, "Erro na abertura.")
        c.refresh_from_db()
        self.assertEqual(c.status, Chamado.Status.CANCELADO)

    def test_cancela_aguardando_coleta(self):
        c = self._chamado(Chamado.Status.AGUARDANDO_COLETA)
        cancelar_chamado(c, self.user, "Transportadora não veio.")
        c.refresh_from_db()
        self.assertEqual(c.status, Chamado.Status.CANCELADO)

    def test_nao_cancela_finalizado(self):
        c = self._chamado(Chamado.Status.FINALIZADO)
        with self.assertRaises(ValidationError):
            cancelar_chamado(c, self.user, "Qualquer motivo.")

    def test_nao_cancela_ja_cancelado(self):
        c = self._chamado(Chamado.Status.CANCELADO)
        with self.assertRaises(ValidationError):
            cancelar_chamado(c, self.user, "Qualquer motivo.")

    def test_motivo_vazio_levanta_erro(self):
        c = self._chamado(Chamado.Status.ABERTO)
        with self.assertRaises(ValidationError):
            cancelar_chamado(c, self.user, "")

    def test_motivo_apenas_espacos_levanta_erro(self):
        c = self._chamado(Chamado.Status.ABERTO)
        with self.assertRaises(ValidationError):
            cancelar_chamado(c, self.user, "   ")