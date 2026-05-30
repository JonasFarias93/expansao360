from __future__ import annotations

from cadastro.models import Categoria, Equipamento, ItemKit, Kit, TipoEquipamento
from django.utils import timezone
from execucao.models import Chamado
from execucao.tests._base import ChamadoBaseTestCase

from chamados.services.chamado_status import recalcular_status


class TestRecalcularStatusService(ChamadoBaseTestCase):
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
            status=Chamado.Status.ABERTO,
        )

    def _ensure_itens_gerados(self) -> None:
        # evita múltiplas gerações no mesmo chamado, se gerar não for idempotente
        if not self.chamado.itens.exists():
            self.chamado.gerar_itens_de_instalacao()

    def _deixar_itens_ok_para_nf(self) -> None:
        """Prepara itens para o gate de NF (mesma regra do pode_liberar_nf)."""
        self._ensure_itens_gerados()

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
        self._ensure_itens_gerados()
        item = self.chamado.itens.first()
        assert item is not None
        item.configurado_em = timezone.now()
        item.save(update_fields=["configurado_em"])

    def test_quando_status_em_abertura_entao_nao_muda(self) -> None:
        self.chamado.status = Chamado.Status.EM_ABERTURA
        self.chamado.save(update_fields=["status"])

        self.assertEqual(
            str(recalcular_status(self.chamado)), str(Chamado.Status.EM_ABERTURA)
        )

    def test_quando_status_aberto_entao_promove_para_em_execucao(self) -> None:
        self.chamado.status = Chamado.Status.ABERTO
        self.chamado.save(update_fields=["status"])

        self.assertEqual(
            str(recalcular_status(self.chamado)), str(Chamado.Status.EM_EXECUCAO)
        )

    def test_quando_item_configurado_e_status_em_execucao_entao_permanece_em_execucao(
        self,
    ) -> None:
        self.chamado.status = Chamado.Status.EM_EXECUCAO
        self.chamado.save(update_fields=["status"])

        self._marcar_um_item_configurado()

        self.assertEqual(
            str(recalcular_status(self.chamado)), str(Chamado.Status.EM_EXECUCAO)
        )

    def test_quando_item_configurado_e_status_aberto_entao_promove_para_em_execucao(
        self,
    ) -> None:
        self.chamado.status = Chamado.Status.ABERTO
        self.chamado.save(update_fields=["status"])

        self._marcar_um_item_configurado()

        self.assertEqual(
            str(recalcular_status(self.chamado)), str(Chamado.Status.EM_EXECUCAO)
        )

    def test_quando_aguardando_nf_entao_nao_regride_mesmo_com_item_configurado(
        self,
    ) -> None:
        self.chamado.status = Chamado.Status.AGUARDANDO_NF
        self.chamado.save(update_fields=["status"])

        self._marcar_um_item_configurado()

        self.assertEqual(
            str(recalcular_status(self.chamado)), str(Chamado.Status.AGUARDANDO_NF)
        )

    def test_quando_aguardando_coleta_entao_nao_regride_mesmo_com_item_configurado(
        self,
    ) -> None:
        self.chamado.status = Chamado.Status.AGUARDANDO_COLETA
        self.chamado.save(update_fields=["status"])

        self._marcar_um_item_configurado()

        self.assertEqual(
            str(recalcular_status(self.chamado)), str(Chamado.Status.AGUARDANDO_COLETA)
        )

    def test_quando_nf_saida_preenchida_em_execucao_entao_promove_para_aguardando_coleta(
        self,
    ) -> None:
        self.chamado.status = Chamado.Status.EM_EXECUCAO
        self.chamado.nf_saida_numero = "12345"
        self.chamado.save(update_fields=["status", "nf_saida_numero"])

        self.assertEqual(
            str(recalcular_status(self.chamado)), str(Chamado.Status.AGUARDANDO_COLETA)
        )

    def test_quando_envio_com_contabil_e_gate_nf_ok_entao_promove_para_aguardando_nf_e_eh_idempotente(
        self,
    ) -> None:
        self.chamado.tipo = Chamado.Tipo.ENVIO
        self.chamado.status = Chamado.Status.EM_EXECUCAO
        self.chamado.contabilidade_numero = "PED-001"
        self.chamado.save(update_fields=["tipo", "status", "contabilidade_numero"])

        self._deixar_itens_ok_para_nf()

        self.assertTrue(self.chamado.pode_liberar_nf())
        self.assertEqual(
            str(recalcular_status(self.chamado)), str(Chamado.Status.AGUARDANDO_NF)
        )

        # idempotência: rodar de novo mantendo as condições não muda
        self.assertTrue(self.chamado.pode_liberar_nf())
        self.assertEqual(
            str(recalcular_status(self.chamado)), str(Chamado.Status.AGUARDANDO_NF)
        )

    def test_quando_perde_condicao_depois_de_aguardando_nf_entao_nao_regride(
        self,
    ) -> None:
        self.chamado.status = Chamado.Status.AGUARDANDO_NF
        self.chamado.contabilidade_numero = None
        self.chamado.save(update_fields=["status", "contabilidade_numero"])

        self.assertEqual(
            str(recalcular_status(self.chamado)), str(Chamado.Status.AGUARDANDO_NF)
        )

    def test_quando_roda_duas_vezes_com_mesmo_estado_entao_e_idempotente(self) -> None:
        self.chamado.status = Chamado.Status.ABERTO
        self.chamado.save(update_fields=["status"])
        s1 = str(recalcular_status(self.chamado))

        self.chamado.status = s1
        self.chamado.save(update_fields=["status"])
        s2 = str(recalcular_status(self.chamado))

        self.assertEqual(s1, s2)
    def test_configurar_item_nao_remove_chamado_da_fila(self) -> None:
        """
        Configurar item NÃO deve mover chamado para fora da fila operacional.
        Fila inclui: ABERTO, EM_EXECUCAO, AGUARDANDO_NF, AGUARDANDO_COLETA.
        """
        from execucao.models import Chamado as ChamadoModel

        STATUS_FILA = {
            ChamadoModel.Status.ABERTO,
            ChamadoModel.Status.EM_EXECUCAO,
            ChamadoModel.Status.AGUARDANDO_NF,
            ChamadoModel.Status.AGUARDANDO_COLETA,
        }

        self.chamado.status = Chamado.Status.EM_EXECUCAO
        self.chamado.save(update_fields=["status"])

        self._marcar_um_item_configurado()

        novo = recalcular_status(self.chamado)
        self.assertIn(novo, STATUS_FILA)
