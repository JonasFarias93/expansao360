from __future__ import annotations

from django.utils import timezone

from cadastro.models import Categoria, Equipamento, TipoEquipamento
from chamados.models import InstalacaoItem
from chamados.services.finalizacao import validar_finalizacao
from execucao.models import Chamado
from execucao.tests._base import ChamadoBaseTestCase


class TestValidarFinalizacaoService(ChamadoBaseTestCase):
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

    def test_quando_coleta_nao_confirmada_entao_retorna_pendencia_coleta_nao_confirmada(
        self,
    ) -> None:
        chamado = self._mk_chamado(
            tipo=Chamado.Tipo.ENVIO,
            contabilidade_numero="123",
            nf_saida_numero="999",
            coleta_confirmada_em=None,
        )

        res = validar_finalizacao(chamado)

        self.assertFalse(res.ok)
        self.assertTrue(any(p.code == "COLETA_NAO_CONFIRMADA" for p in res.coleta))

    def test_quando_tipo_envio_sem_nf_e_sem_contabil_entao_retorna_pendencias_fiscais(
        self,
    ) -> None:
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

    def test_quando_nf_saida_contem_letras_entao_retorna_pendencia_nf_invalida(
        self,
    ) -> None:
        chamado = self._mk_chamado(
            tipo=Chamado.Tipo.ENVIO,
            contabilidade_numero="123",
            nf_saida_numero="12A",
            coleta_confirmada_em=timezone.now(),
        )

        res = validar_finalizacao(chamado)

        self.assertFalse(res.ok)
        self.assertTrue(any(p.code == "FISCAL_NF_SAIDA_INVALIDA" for p in res.fiscais))


class TestFinalizacaoNaoExigirAtivoParaHub(ChamadoBaseTestCase):
    def test_quando_equipamento_nao_tem_ativo_entao_nao_cria_pendencia_de_ativo_nem_serial(
        self,
    ) -> None:
        cat = Categoria.objects.create(nome="Informatica")
        TipoEquipamento.objects.create(categoria=cat, nome="PERIF")

        hub = Equipamento.objects.create(
            codigo="03",
            nome="HUb",
            categoria=cat,
            tem_ativo=False,
        )

        ch = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            protocolo="T1",
            tipo=Chamado.Tipo.ENVIO,
            status=Chamado.Status.EM_ABERTURA,
            coleta_confirmada_em=timezone.now(),
        )

        InstalacaoItem.objects.create(
            chamado=ch,
            equipamento=hub,
            tipo="periferico (PERIFERICO)",
            quantidade=1,
            tem_ativo=False,
            ativo="",
            numero_serie="",
        )

        res = validar_finalizacao(ch)
        msgs = [p.message for p in res.itens]

        self.assertNotIn("Item rastreável exige ATIVO preenchido.", msgs)
        self.assertNotIn("Item rastreável exige SERIAL preenchido.", msgs)

        def test_quando_equipamento_tem_ativo_entao_exige_ativo_e_numero_serie(
            self,
        ) -> None:
            cat = Categoria.objects.create(nome="Informatica")
            TipoEquipamento.objects.create(categoria=cat, nome="TC")
            eq = Equipamento.objects.create(
                codigo="X", nome="Rastreavel", categoria=cat, tem_ativo=True
            )

            ch = self._mk_chamado(
                coleta_confirmada_em=timezone.now(),
                contabilidade_numero="1",
                nf_saida_numero="2",
            )
            InstalacaoItem.objects.create(
                chamado=ch,
                equipamento=eq,
                tipo="tc (TC)",
                quantidade=1,
                tem_ativo=True,
                ativo="",
                numero_serie="",
            )

            res = validar_finalizacao(ch)
            msgs = [p.message for p in res.itens]
            self.assertIn("Item rastreável exige ATIVO preenchido.", msgs)
            self.assertIn("Item rastreável exige SERIAL preenchido.", msgs)
