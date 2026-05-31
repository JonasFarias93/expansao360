# web/historico/tests/test_services_projecao.py
from __future__ import annotations

from django.utils import timezone

from chamados.models import Chamado, InstalacaoItem
from chamados.tests._base import WebAuthBaseTestCase
from cadastro.models import Categoria, Equipamento, ItemKit, TipoEquipamento
from historico.models import HistoricoExecucao, HistoricoAtivoTimeline
from historico.services.projecao import gerar_historico_execucao


class TestGerarHistoricoExecucao(WebAuthBaseTestCase):

    def setUp(self):
        super().setUp()
        self.categoria = Categoria.objects.get_or_create(nome="Infra")[0]
        self.tipo = TipoEquipamento.objects.create(categoria=self.categoria, nome="PDV")
        self.eq = Equipamento.objects.create(
            nome="Micro", categoria=self.categoria, tem_ativo=True
        )
        ItemKit.objects.create(
            kit=self.kit, equipamento=self.eq, tipo=self.tipo, quantidade=1
        )
        self.chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            status=Chamado.Status.FINALIZADO,
            finalizado_em=timezone.now(),
        )
        self.chamado.gerar_itens_de_instalacao()

    def test_gera_historico_execucao(self):
        h = gerar_historico_execucao(self.chamado)
        self.assertEqual(h.chamado_id, self.chamado.pk)
        self.assertEqual(h.protocolo, self.chamado.protocolo)
        self.assertEqual(h.loja_codigo, self.loja.codigo)
        self.assertEqual(h.status_final, Chamado.Status.FINALIZADO)

    def test_idempotente(self):
        gerar_historico_execucao(self.chamado)
        gerar_historico_execucao(self.chamado)
        self.assertEqual(HistoricoExecucao.objects.filter(chamado_id=self.chamado.pk).count(), 1)

    def test_itens_snapshot_gerado(self):
        h = gerar_historico_execucao(self.chamado)
        self.assertIsInstance(h.itens_snapshot, list)
        self.assertEqual(len(h.itens_snapshot), self.chamado.itens.count())

    def test_timeline_ativo_gerada_para_item_bipado(self):
        item = self.chamado.itens.first()
        item.ativo = "ATV-001"
        item.numero_serie = "SN-001"
        item.save(update_fields=["ativo", "numero_serie"])

        gerar_historico_execucao(self.chamado)

        self.assertTrue(
            HistoricoAtivoTimeline.objects.filter(
                ativo="ATV-001", chamado_id=self.chamado.pk
            ).exists()
        )

    def test_timeline_nao_gerada_para_item_sem_ativo(self):
        gerar_historico_execucao(self.chamado)
        self.assertEqual(
            HistoricoAtivoTimeline.objects.filter(chamado_id=self.chamado.pk).count(), 0
        )

    def test_signal_dispara_ao_finalizar(self):
        chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            status=Chamado.Status.ABERTO,
        )
        chamado.status = Chamado.Status.FINALIZADO
        chamado.finalizado_em = timezone.now()
        chamado.save(update_fields=["status", "finalizado_em"])

        self.assertTrue(
            HistoricoExecucao.objects.filter(chamado_id=chamado.pk).exists()
        )