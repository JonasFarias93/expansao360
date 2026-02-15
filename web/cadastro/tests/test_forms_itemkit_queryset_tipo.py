from __future__ import annotations

from django.test import TestCase

from cadastro.forms import ItemKitForm
from cadastro.models import Categoria, Equipamento, ItemKit, Kit, TipoEquipamento


class TestItemKitFormTipoQueryset(TestCase):
    def setUp(self) -> None:
        self.categoria = Categoria.objects.create(nome="Cat A", disponivel=True)

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

    def test_quando_edicao_entao_queryset_tipo_reflete_categoria_e_initial(
        self,
    ) -> None:
        item = ItemKit.objects.create(
            kit=self.kit,
            equipamento=self.equip,
            tipo=self.tipo_a,
            quantidade=1,
            requer_configuracao=False,
        )

        form = ItemKitForm(instance=item)

        qs = list(form.fields["tipo"].queryset)
        self.assertIn(self.tipo_a, qs)
        self.assertIn(self.tipo_b, qs)
        self.assertNotIn(self.tipo_off, qs)

        self.assertEqual(form.initial.get("tipo"), self.tipo_a.id)

    def test_quando_post_com_equipamento_entao_queryset_tipo_filtra_por_categoria(
        self,
    ) -> None:
        prefix = "itens-0"
        data = {
            f"{prefix}-equipamento": str(self.equip.id),
            f"{prefix}-tipo": str(self.tipo_b.id),
            f"{prefix}-quantidade": "2",
        }

        form = ItemKitForm(data=data, prefix=prefix)

        qs = list(form.fields["tipo"].queryset)
        self.assertIn(self.tipo_a, qs)
        self.assertIn(self.tipo_b, qs)
        self.assertNotIn(self.tipo_off, qs)

    def test_quando_post_com_equipamento_invalido_entao_queryset_tipo_fica_vazio(
        self,
    ) -> None:
        prefix = "itens-0"
        data = {
            f"{prefix}-equipamento": "999999",
            f"{prefix}-tipo": "",
            f"{prefix}-quantidade": "1",
        }

        form = ItemKitForm(data=data, prefix=prefix)
        self.assertEqual(form.fields["tipo"].queryset.count(), 0)
