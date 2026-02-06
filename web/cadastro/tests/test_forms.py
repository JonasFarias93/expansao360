from django.test import TestCase

from cadastro.forms import ProjetoForm

# ==========================
#  Form /cadasto / Loja
# ==========================


class LojaFormTest(TestCase):
    def test_loja_form_labels(self) -> None:
        from cadastro.forms import LojaForm

        form = LojaForm()
        self.assertEqual(form.fields["codigo"].label, "Java")
        self.assertEqual(form.fields["nome"].label, "Nome loja")
        self.assertIn("ip_banco_12", form.fields)


def test_projeto_form_expoe_cor_slug():
    form = ProjetoForm()
    assert "cor_slug" in form.fields
