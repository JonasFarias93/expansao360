from __future__ import annotations

from cadastro.models import Categoria, Equipamento, ItemKit, Kit, TipoEquipamento
from chamados.services.chamado_status import recalcular_status
from django.utils import timezone

from execucao.models import Chamado
from execucao.tests._base import ChamadoBaseTestCase


class RecalcularStatusServiceTests(ChamadoBaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        # sobrescreve o kit básico com um kit que realmente gera itens
        self.categoria = Categoria.objects.create(nome="Informatica")
        self.tipo = TipoEquipamento.objects.create(categoria=self.categoria, nome="TC")
        self.kit = Kit.objects.create(nome="Kit Gate NF")

        # rastreável
        self.eq_micro = Equipamento.objects.create(
            codigo="MICRO_TC",
            nome="Micro TC",
            categoria=self.categoria,
            tem_ativo=True,
            configuravel=True,
        )

        # contável (acessório)
        self.eq_mouse = Equipamento.objects.create(
            codigo="MOUSE",
            nome="Mouse",
            categoria=self.categoria,
            tem_ativo=False,
            configuravel=False,
        )

        # itens do kit (2 unidades do rastreável + 2 do contável, igual o gate costuma fazer)
        ItemKit.objects.create(
            kit=self.kit,
            tipo=self.tipo,
            equipamento=self.eq_micro,
            quantidade=2,
            requer_configuracao=False,
        )
        ItemKit.objects.create(
            kit=self.kit,
            tipo=self.tipo,
            equipamento=self.eq_mouse,
            quantidade=2,
            requer_configuracao=False,
        )

        self.chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            status="ABERTO",
        )

    def _deixar_itens_ok_para_nf(self) -> None:
        """Prepara itens para o gate de NF (mesma regra do test_models_chamado_nf_gate)."""
        self.chamado.gerar_itens_de_instalacao()

        for item in self.chamado.itens.all():
            if item.tem_ativo:
                item.ativo = "ATV-123"
                item.numero_serie = "SN-123"
                item.save(update_fields=["ativo", "numero_serie"])
            else:
                item.confirmado = True
                item.save(update_fields=["confirmado"])

    def _marcar_um_item_configurado(self) -> None:
        """Marca pelo menos um item como configurado (sinal para EM_CONFIGURACAO)."""
        self.chamado.gerar_itens_de_instalacao()
        item = self.chamado.itens.first()
        assert item is not None
        item.configurado_em = timezone.now()
        item.save(update_fields=["configurado_em"])

    def test_nao_mexe_em_em_abertura(self) -> None:
        self.chamado.status = "EM_ABERTURA"
        self.chamado.save(update_fields=["status"])
        self.assertEqual(str(recalcular_status(self.chamado)), "EM_ABERTURA")

    def test_primeiro_save_promove_aberto_para_em_execucao(self) -> None:
        self.chamado.status = "ABERTO"
        self.chamado.save(update_fields=["status"])
        self.assertEqual(str(recalcular_status(self.chamado)), "EM_EXECUCAO")

    def test_item_configurado_promove_para_em_configuracao_quando_em_execucao(self) -> None:
        self.chamado.status = "EM_EXECUCAO"
        self.chamado.save(update_fields=["status"])

        self._marcar_um_item_configurado()

        self.assertEqual(str(recalcular_status(self.chamado)), "EM_CONFIGURACAO")

    def test_item_configurado_promove_para_em_configuracao_quando_aberto(self) -> None:
        self.chamado.status = "ABERTO"
        self.chamado.save(update_fields=["status"])

        self._marcar_um_item_configurado()

        self.assertEqual(str(recalcular_status(self.chamado)), "EM_CONFIGURACAO")

    def test_item_configurado_nao_regride_quando_aguardando_nf(self) -> None:
        self.chamado.status = "AGUARDANDO_NF"
        self.chamado.save(update_fields=["status"])

        self._marcar_um_item_configurado()

        self.assertEqual(str(recalcular_status(self.chamado)), "AGUARDANDO_NF")

    def test_item_configurado_nao_regride_quando_aguardando_coleta(self) -> None:
        self.chamado.status = "AGUARDANDO_COLETA"
        self.chamado.save(update_fields=["status"])

        self._marcar_um_item_configurado()

        self.assertEqual(str(recalcular_status(self.chamado)), "AGUARDANDO_COLETA")

    def test_nf_saida_preenchida_promove_para_aguardando_coleta(self) -> None:
        self.chamado.status = "EM_EXECUCAO"
        self.chamado.nf_saida_numero = "12345"
        self.chamado.save(update_fields=["status", "nf_saida_numero"])
        self.assertEqual(str(recalcular_status(self.chamado)), "AGUARDANDO_COLETA")

    def test_contabil_e_gate_nf_promove_para_aguardando_nf(self) -> None:
        self.chamado.tipo = Chamado.Tipo.ENVIO
        self.chamado.status = "EM_EXECUCAO"
        self.chamado.contabilidade_numero = "PED-001"
        self.chamado.save(update_fields=["tipo", "status", "contabilidade_numero"])

        self._deixar_itens_ok_para_nf()

        self.assertTrue(self.chamado.pode_liberar_nf())
        self.assertEqual(str(recalcular_status(self.chamado)), "AGUARDANDO_NF")

        # idempotência: rodar de novo mantendo as condições não muda
        self.assertTrue(self.chamado.pode_liberar_nf())
        self.assertEqual(str(recalcular_status(self.chamado)), "AGUARDANDO_NF")

    def test_nunca_regride(self) -> None:
        self.chamado.status = "AGUARDANDO_NF"
        self.chamado.contabilidade_numero = None
        self.chamado.save(update_fields=["status", "contabilidade_numero"])
        self.assertEqual(str(recalcular_status(self.chamado)), "AGUARDANDO_NF")

    def test_idempotente(self) -> None:
        self.chamado.status = "ABERTO"
        self.chamado.save(update_fields=["status"])
        s1 = str(recalcular_status(self.chamado))

        self.chamado.status = s1
        self.chamado.save(update_fields=["status"])
        s2 = str(recalcular_status(self.chamado))

        self.assertEqual(s1, s2)
