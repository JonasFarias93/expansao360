from django.test import TestCase

from cadastro.models import Categoria, TipoEquipamento


class TestTipoEquipamentoCodigo(TestCase):
    def test_quando_codigo_vazio_entao_gera_automaticamente(self) -> None:
        cat = Categoria.objects.create(nome="Monitores")
        t = TipoEquipamento.objects.create(categoria=cat, nome="Touch")
        self.assertEqual(t.codigo, "TOUCH")

    def test_quando_colisao_na_mesma_categoria_entao_sufixa(self) -> None:
        cat = Categoria.objects.create(nome="Monitores")
        t1 = TipoEquipamento.objects.create(categoria=cat, nome="LCD")
        t2 = TipoEquipamento.objects.create(categoria=cat, nome="LCD")
        self.assertEqual(t1.codigo, "LCD")
        self.assertEqual(t2.codigo, "LCD_2")

    def test_quando_mesmo_nome_em_categorias_diferentes_entao_codigo_pode_repetir(
        self,
    ) -> None:
        c1 = Categoria.objects.create(nome="Monitores")
        c2 = Categoria.objects.create(nome="Microcomputadores")

        t1 = TipoEquipamento.objects.create(categoria=c1, nome="PDV")
        t2 = TipoEquipamento.objects.create(categoria=c2, nome="PDV")

        self.assertEqual(t1.codigo, "PDV")
        self.assertEqual(t2.codigo, "PDV")

    def test_str_retorna_nome_e_codigo(self) -> None:
        cat = Categoria.objects.create(nome="Monitores")
        t = TipoEquipamento.objects.create(categoria=cat, nome="Touch")
        self.assertIn("Touch", str(t))
        self.assertIn("TOUCH", str(t))
