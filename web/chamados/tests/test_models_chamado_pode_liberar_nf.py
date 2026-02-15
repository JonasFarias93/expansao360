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
from django.test import TestCase
from execucao.models import Chamado


class TestChamadoPodeLiberarNF(TestCase):
    def setUp(self) -> None:
        self.categoria = Categoria.objects.create(nome="Informatica")
        self.tipo = TipoEquipamento.objects.create(categoria=self.categoria, nome="TC")

        # rastreável
        self.eq_rastreavel = Equipamento.objects.create(
            codigo="MICRO_TC",
            nome="Micro TC",
            categoria=self.categoria,
            tem_ativo=True,
            configuravel=True,
        )

        # contável (acessório)
        self.eq_contavel = Equipamento.objects.create(
            codigo="TECLADO",
            nome="Teclado",
            categoria=self.categoria,
            tem_ativo=False,
            configuravel=False,
        )

        self.kit = Kit.objects.create(nome="Kit TC")
        ItemKit.objects.create(
            kit=self.kit,
            equipamento=self.eq_rastreavel,
            tipo=self.tipo,
            quantidade=1,
            requer_configuracao=False,
        )
        ItemKit.objects.create(
            kit=self.kit,
            equipamento=self.eq_contavel,
            tipo=self.tipo,
            quantidade=2,
            requer_configuracao=False,
        )

        self.loja = Loja.objects.create(codigo="001", nome="Loja 001")
        self.projeto = Projeto.objects.create(codigo="P1", nome="Projeto 1")
        self.subprojeto = Subprojeto.objects.create(
            projeto=self.projeto, codigo="SP1", nome="Sub 1"
        )

    def _criar_chamado_envio(self) -> Chamado:
        return Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.subprojeto,
            kit=self.kit,
            tipo=Chamado.Tipo.ENVIO,
        )

    def _criar_chamado_envio_com_itens(self) -> Chamado:
        chamado = self._criar_chamado_envio()
        chamado.gerar_itens_de_instalacao()
        return chamado

    def _bipar_itens_rastreaveis(self, chamado: Chamado) -> None:
        for item in chamado.itens.all():
            if item.tem_ativo:
                item.ativo = "ATV-123"
                item.numero_serie = "SN-123"
                item.save(update_fields=["ativo", "numero_serie"])

    def _confirmar_itens_contaveis(self, chamado: Chamado) -> None:
        for item in chamado.itens.all():
            if not item.tem_ativo:
                item.confirmado = True
                item.save(update_fields=["confirmado"])

    def test_quando_envio_sem_itens_entao_nao_pode_liberar_nf(self) -> None:
        chamado = self._criar_chamado_envio()
        self.assertFalse(chamado.pode_liberar_nf())

    def test_quando_falta_bipagem_do_rastreavel_entao_nao_pode_liberar_nf(self) -> None:
        chamado = self._criar_chamado_envio_com_itens()

        # confirma apenas os contáveis
        self._confirmar_itens_contaveis(chamado)

        self.assertFalse(chamado.pode_liberar_nf())

    def test_quando_falta_confirmacao_do_contavel_entao_nao_pode_liberar_nf(
        self,
    ) -> None:
        chamado = self._criar_chamado_envio_com_itens()

        # bipagem do rastreável ok, mas não confirma contáveis
        self._bipar_itens_rastreaveis(chamado)

        self.assertFalse(chamado.pode_liberar_nf())

    def test_quando_rastreaveis_bipados_e_contaveis_confirmados_entao_pode_liberar_nf(
        self,
    ) -> None:
        chamado = self._criar_chamado_envio_com_itens()

        self._bipar_itens_rastreaveis(chamado)
        self._confirmar_itens_contaveis(chamado)

        self.assertTrue(chamado.pode_liberar_nf())
