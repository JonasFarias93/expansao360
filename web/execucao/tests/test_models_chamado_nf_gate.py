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


class ChamadoGateNFTests(TestCase):
    def setUp(self) -> None:
        self.categoria = Categoria.objects.create(nome="Informatica")
        self.tipo = TipoEquipamento.objects.create(categoria=self.categoria, nome="TC")

        # rastreável
        self.eq_micro = Equipamento.objects.create(
            codigo="MICRO_TC",
            nome="Micro TC",
            categoria=self.categoria,
            tem_ativo=True,
            configuravel=True,
        )

        # contável (acessório)
        self.eq_teclado = Equipamento.objects.create(
            codigo="TECLADO",
            nome="Teclado",
            categoria=self.categoria,
            tem_ativo=False,
            configuravel=False,
        )

        self.kit = Kit.objects.create(nome="Kit TC")
        ItemKit.objects.create(
            kit=self.kit,
            equipamento=self.eq_micro,
            tipo=self.tipo,
            quantidade=1,
            requer_configuracao=False,
        )
        ItemKit.objects.create(
            kit=self.kit,
            equipamento=self.eq_teclado,
            tipo=self.tipo,
            quantidade=2,
            requer_configuracao=False,
        )

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
        )
        chamado.gerar_itens_de_instalacao()
        return chamado

    def test_pode_liberar_nf_false_quando_sem_itens(self):
        chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.subprojeto,
            kit=self.kit,
            tipo=Chamado.Tipo.ENVIO,
        )
        self.assertFalse(chamado.pode_liberar_nf())

    def test_pode_liberar_nf_false_quando_falta_bipagem(self):
        chamado = self._criar_chamado_envio_com_itens()

        # Não preenche ativo/serial do rastreável
        # Confirma o contável (simula check na caixa)
        for item in chamado.itens.all():
            if not item.tem_ativo:
                item.confirmado = True
                item.save(update_fields=["confirmado"])

        self.assertFalse(chamado.pode_liberar_nf())

    def test_pode_liberar_nf_false_quando_falta_checagem(self):
        chamado = self._criar_chamado_envio_com_itens()

        # Bipagem do rastreável ok
        for item in chamado.itens.all():
            if item.tem_ativo:
                item.ativo = "ATV-123"
                item.numero_serie = "SN-123"
                item.save(update_fields=["ativo", "numero_serie"])

        # não confirma o contável
        self.assertFalse(chamado.pode_liberar_nf())

    def test_pode_liberar_nf_true_quando_itens_bipados_e_checados(self):
        chamado = self._criar_chamado_envio_com_itens()

        for item in chamado.itens.all():
            if item.tem_ativo:
                item.ativo = "ATV-123"
                item.numero_serie = "SN-123"
                item.save(update_fields=["ativo", "numero_serie"])
            else:
                item.confirmado = True
                item.save(update_fields=["confirmado"])

        self.assertTrue(chamado.pode_liberar_nf())
