from __future__ import annotations

from chamados.services.finalizacao import validar_finalizacao
from django.utils import timezone

from execucao.models import Chamado
from execucao.tests._base import ChamadoBaseTestCase


class ValidarFinalizacaoServiceTests(ChamadoBaseTestCase):
    def _mk_chamado(
        self,
        *,
        tipo: str = Chamado.Tipo.ENVIO,
        status: str = Chamado.Status.AGUARDANDO_COLETA,
        contabilidade_numero: str = "",
        nf_saida_numero: str = "",
        coleta_confirmada_em=None,
    ) -> Chamado:
        return Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            tipo=tipo,
            status=status,
            contabilidade_numero=contabilidade_numero,
            nf_saida_numero=nf_saida_numero,
            coleta_confirmada_em=coleta_confirmada_em,
        )

    def test_pendente_quando_coleta_nao_confirmada(self) -> None:
        chamado = self._mk_chamado(
            tipo=Chamado.Tipo.ENVIO,
            contabilidade_numero="123",
            nf_saida_numero="999",
            coleta_confirmada_em=None,
        )

        res = validar_finalizacao(chamado)

        self.assertFalse(res.ok)
        self.assertTrue(any(p.code == "COLETA_NAO_CONFIRMADA" for p in res.coleta))

    def test_envio_exige_nf_e_contabil(self) -> None:
        chamado = self._mk_chamado(
            tipo=Chamado.Tipo.ENVIO,
            contabilidade_numero="",
            nf_saida_numero="",
            coleta_confirmada_em=timezone.now(),
        )

        res = validar_finalizacao(chamado)

        self.assertFalse(res.ok)
        self.assertTrue(any(p.code == "FISCAL_FALTA_CONTABIL" for p in res.fiscais))
        self.assertTrue(any(p.code == "FISCAL_FALTA_NF_SAIDA" for p in res.fiscais))

    def test_nf_apenas_digitos(self) -> None:
        chamado = self._mk_chamado(
            tipo=Chamado.Tipo.ENVIO,
            contabilidade_numero="123",
            nf_saida_numero="12A",
            coleta_confirmada_em=timezone.now(),
        )

        res = validar_finalizacao(chamado)

        self.assertFalse(res.ok)
        self.assertTrue(any(p.code == "FISCAL_NF_SAIDA_INVALIDA" for p in res.fiscais))
