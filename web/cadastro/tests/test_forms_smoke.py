from __future__ import annotations

from django.test import TestCase

from cadastro.forms import LojaForm, ProjetoForm


class TestLojaFormSmoke(TestCase):
    def test_quando_instancia_form_entao_labels_e_campos_existem(self) -> None:
        form = LojaForm()
        self.assertEqual(form.fields["codigo"].label, "Java")
        self.assertEqual(form.fields["nome"].label, "Nome loja")
        self.assertIn("ip_banco_12", form.fields)


class TestProjetoFormSmoke(TestCase):
    def test_quando_instancia_form_entao_expoe_cor_slug(self) -> None:
        form = ProjetoForm()
        self.assertIn("cor_slug", form.fields)
