from __future__ import annotations

from cadastro.models import (
    Categoria,
    Equipamento,
    ItemKit,
    Kit,
    Loja,
    Projeto,
    Subprojeto,
    TipoEquipamento,
)
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from execucao.models import Chamado, StatusConfiguracao


class TestChamadoFinalizarExigeConfiguracaoQuandoItemMarcado(TestCase):
    def setUp(self) -> None:
        # base cadastro
        self.categoria = Categoria.objects.create(nome="Informatica")

        # TipoEquipamento (ex: "TC")
        self.tipo = TipoEquipamento.objects.create(categoria=self.categoria, nome="TC")

        # Equipamento configurável e rastreável (tem ativo)
        self.eq_micro = Equipamento.objects.create(
            codigo="MICRO_TC",
            nome="Micro TC",
            categoria=self.categoria,
            tem_ativo=True,
            configuravel=True,
        )

        # Kit + ItemKit
        self.kit = Kit.objects.create(nome="Kit TC")
        ItemKit.objects.create(
            kit=self.kit,
            equipamento=self.eq_micro,
            tipo=self.tipo,
            quantidade=1,
            # cadastro não deve obrigar configuração
            requer_configuracao=False,
        )

        # Loja / Projeto / Subprojeto
        self.loja = Loja.objects.create(codigo="001", nome="Loja 001")
        self.projeto = Projeto.objects.create(codigo="P1", nome="Projeto 1")
        self.subprojeto = Subprojeto.objects.create(
            projeto=self.projeto, codigo="SP1", nome="Sub 1"
        )

    def _criar_chamado_envio_com_itens(self) -> Chamado:
        chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.subprojeto,
            kit=self.kit,
            tipo=Chamado.Tipo.ENVIO,
            nf_saida_numero="NF-123",
            coleta_confirmada_em=timezone.now(),
        )
        chamado.gerar_itens_de_instalacao()
        return chamado

    def _bipar_todos_os_itens(self, chamado: Chamado) -> None:
        for item in chamado.itens.all():
            if item.tem_ativo:
                item.ativo = "ATV-123"
                item.numero_serie = "SN-123"
                item.save(update_fields=["ativo", "numero_serie"])
            else:
                item.confirmado = True
                item.save(update_fields=["confirmado"])

    def _liberar_gates_envio(self, chamado: Chamado) -> None:
        chamado.nf_saida_numero = "NF-123"
        chamado.coleta_confirmada_em = timezone.now()
        chamado.save(update_fields=["nf_saida_numero", "coleta_confirmada_em"])

    def test_quando_item_nao_marcado_para_configurar_entao_ip_nao_e_exigido(
        self,
    ) -> None:
        chamado = self._criar_chamado_envio_com_itens()
        self._bipar_todos_os_itens(chamado)
        self._liberar_gates_envio(chamado)

        item = chamado.itens.get()

        self.assertFalse(item.deve_configurar)

        # não marcamos pra configurar => deve finalizar sem exigir IP/configuração
        chamado.finalizar()

    def test_quando_item_marcado_para_configurar_entao_exige_status_configurado_e_ip(
        self,
    ) -> None:
        chamado = self._criar_chamado_envio_com_itens()
        self._bipar_todos_os_itens(chamado)
        self._liberar_gates_envio(chamado)

        item = chamado.itens.get()

        item.deve_configurar = True
        item.save(update_fields=["deve_configurar"])

        # 1) Sem status CONFIGURADO => deve falhar
        with self.assertRaises(ValidationError):
            chamado.finalizar()

        # 2) Com status CONFIGURADO mas sem IP => deve falhar
        item.status_configuracao = StatusConfiguracao.CONFIGURADO
        item.save(update_fields=["status_configuracao"])

        with self.assertRaises(ValidationError):
            chamado.finalizar()

        # 3) Com status CONFIGURADO e IP => deve passar
        item.ip = "10.0.0.10"
        item.save(update_fields=["ip"])

        chamado.finalizar()
