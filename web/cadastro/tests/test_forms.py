from __future__ import annotations

from django.test import TestCase

from cadastro.forms import ItemKitForm, LojaForm, ProjetoForm
from cadastro.models import Categoria, Equipamento, ItemKit, Kit, TipoEquipamento


class LojaFormTest(TestCase):
    def test_loja_form_labels(self) -> None:
        form = LojaForm()
        self.assertEqual(form.fields["codigo"].label, "Java")
        self.assertEqual(form.fields["nome"].label, "Nome loja")
        self.assertIn("ip_banco_12", form.fields)


class ProjetoFormTest(TestCase):
    def test_projeto_form_expoe_cor_slug(self) -> None:
        form = ProjetoForm()
        self.assertIn("cor_slug", form.fields)


class ItemKitFormTest(TestCase):
    def setUp(self) -> None:
        self.categoria = Categoria.objects.create(nome="Cat A", disponivel=True)

        # Tipos disponíveis para a categoria
        self.tipo_a = TipoEquipamento.objects.create(
            nome="Tipo A",
            categoria=self.categoria,
            disponivel=True,
        )
        self.tipo_b = TipoEquipamento.objects.create(
            nome="Tipo B",
            categoria=self.categoria,
            disponivel=True,
        )

        # Tipo indisponível (não deve aparecer)
        self.tipo_off = TipoEquipamento.objects.create(
            nome="Tipo OFF",
            categoria=self.categoria,
            disponivel=False,
        )

        self.equip = Equipamento.objects.create(
            nome="Equip A",
            categoria=self.categoria,
            tem_ativo=True,
            configuravel=False,
        )

        self.kit = Kit.objects.create(nome="Kit A")

    def test_itemkit_form_edicao_preenche_queryset_tipo(self) -> None:
        """
        Ao editar (instance.pk), o form deve popular o queryset de 'tipo' com os tipos
        da categoria do equipamento, e conter o tipo atualmente selecionado.
        """
        item = ItemKit.objects.create(
            kit=self.kit,
            equipamento=self.equip,
            tipo=self.tipo_a,
            quantidade=1,
            requer_configuracao=False,
        )

        form = ItemKitForm(instance=item)

        qs = form.fields["tipo"].queryset
        self.assertIn(self.tipo_a, list(qs))
        self.assertIn(self.tipo_b, list(qs))
        self.assertNotIn(self.tipo_off, list(qs))

        # E o initial deve refletir o tipo do item
        self.assertEqual(form.initial.get("tipo"), self.tipo_a.id)

    def test_itemkit_form_post_filtra_tipos_por_equipamento(self) -> None:
        """
        Ao submeter (POST) com equipamento escolhido, o form deve filtrar o queryset
        de 'tipo' pela categoria desse equipamento.
        """
        # Importante: simular prefix de formset
        prefix = "itens-0"
        data = {
            f"{prefix}-equipamento": str(self.equip.id),
            f"{prefix}-tipo": str(self.tipo_b.id),
            f"{prefix}-quantidade": "2",
            # checkbox pode vir ausente (False) ou "on" (True); não é o foco aqui
        }

        form = ItemKitForm(data=data, prefix=prefix)

        qs = form.fields["tipo"].queryset
        self.assertIn(self.tipo_a, list(qs))
        self.assertIn(self.tipo_b, list(qs))
        self.assertNotIn(self.tipo_off, list(qs))

    def test_itemkit_form_post_equipamento_invalido_deixa_tipo_vazio(self) -> None:
        """
        Se equipamento_id for inválido ou não existir, deve manter queryset de tipo vazio,
        evitando que o usuário selecione um tipo incorreto.
        """
        prefix = "itens-0"
        data = {
            f"{prefix}-equipamento": "999999",
            f"{prefix}-tipo": "",
            f"{prefix}-quantidade": "1",
        }

        form = ItemKitForm(data=data, prefix=prefix)
        self.assertEqual(form.fields["tipo"].queryset.count(), 0)
