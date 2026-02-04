# web/cadastro/forms.py
from __future__ import annotations

from django import forms
from django.forms import inlineformset_factory
from django.urls import reverse_lazy

from .models import (
    Categoria,
    Equipamento,
    ItemKit,
    Kit,
    Loja,
    Projeto,
    Subprojeto,
    TipoEquipamento,
)

# ==========================
# Tailwind helpers (MVP)
# ==========================
BASE_INPUT_CSS = (
    "w-full rounded-lg border border-slate-300 px-3 py-2 "
    "focus:outline-none focus:ring-2 focus:ring-slate-900"
)
BASE_SELECT_CSS = BASE_INPUT_CSS
BASE_CHECKBOX_CSS = "h-4 w-4 rounded border-slate-300"


def apply_tailwind_styles(form: forms.Form) -> None:
    """
    Aplica classes padrão para manter os templates simples.
    Não mexe em hidden fields.
    """
    for _name, field in form.fields.items():
        widget = field.widget

        if isinstance(widget, forms.CheckboxInput):
            widget.attrs["class"] = BASE_CHECKBOX_CSS
            continue

        # ✅ Python 3.10+: `isinstance` aceita `X | Y`
        if isinstance(widget, forms.Select | forms.SelectMultiple):
            widget.attrs["class"] = BASE_SELECT_CSS
            continue

        # default: text/number/etc
        if not isinstance(widget, forms.HiddenInput):
            widget.attrs["class"] = BASE_INPUT_CSS


# ==========================
# Forms
# ==========================
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nome"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_tailwind_styles(self)


class LojaForm(forms.ModelForm):
    LOGOMARCA_CHOICES = [
        ("RAIA", "RAIA"),
        ("DROGASIL", "DROGASIL"),
    ]

    logomarca = forms.ChoiceField(
        choices=[("", "---------")] + LOGOMARCA_CHOICES,
        required=False,
        label="Logomarca",
    )

    class Meta:
        model = Loja
        fields = [
            "codigo",
            "nome",
            "hist",
            "endereco",
            "bairro",
            "cidade",
            "uf",
            "logomarca",
            "telefone",
            "ip_banco_12",
        ]
        labels = {
            "codigo": "Java",
            "nome": "Nome loja",
            "hist": "Hist.",
            "endereco": "Endereço",
            "bairro": "Bairro",
            "cidade": "Cidade",
            "uf": "UF",
            "logomarca": "Logomarca",
            "telefone": "Telefone",
            "ip_banco_12": "IP Banco 12",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_tailwind_styles(self)


class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = ["codigo", "nome"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_tailwind_styles(self)


class SubprojetoForm(forms.ModelForm):
    class Meta:
        model = Subprojeto
        fields = ["projeto", "codigo", "nome"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # UX: ordenar projetos no select
        self.fields["projeto"].queryset = Projeto.objects.order_by("codigo", "nome")

        apply_tailwind_styles(self)


class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        fields = ["codigo", "nome", "categoria", "tem_ativo", "configuravel"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # UX: ordenar categorias no select
        self.fields["categoria"].queryset = Categoria.objects.order_by("nome")

        apply_tailwind_styles(self)


class KitForm(forms.ModelForm):
    class Meta:
        model = Kit
        fields = ["nome"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_tailwind_styles(self)


class ItemKitForm(forms.ModelForm):
    class Meta:
        model = ItemKit
        fields = ["equipamento", "tipo", "quantidade", "requer_configuracao"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["equipamento"].widget.attrs.update(
            {
                "hx-get": reverse_lazy("registry:ajax_tipos_por_equipamento"),
                "hx-trigger": "change",
                "hx-target": f"#id_{self.prefix}-tipo",
                "hx-swap": "innerHTML",
            }
        )

        # default: vazio (evita escolher tipo errado antes de selecionar equipamento)
        self.fields["tipo"].queryset = TipoEquipamento.objects.none()

        def _set_tipos_por_equipamento(equip: Equipamento | None) -> None:
            """
            TipoEquipamento pertence a Categoria, então filtramos por:
              equipamento.categoria -> tipos ativos
            """
            if not equip or not getattr(equip, "categoria_id", None):
                self.fields["tipo"].queryset = TipoEquipamento.objects.none()
                return

            self.fields["tipo"].queryset = TipoEquipamento.objects.filter(
                categoria_id=equip.categoria_id,
                ativo=True,
            ).order_by("nome")

        # Caso 1: edição (instance já tem equipamento)
        equipamento = getattr(self.instance, "equipamento", None)
        if equipamento is not None and getattr(equipamento, "id", None):
            _set_tipos_por_equipamento(equipamento)

        # Caso 2: POST (usuário selecionou equipamento no form)
        if self.data:
            equipamento_key = f"{self.prefix}-equipamento"
            equip_id = self.data.get(equipamento_key)

            if equip_id:
                try:
                    equip = Equipamento.objects.select_related("categoria").get(id=int(equip_id))
                    _set_tipos_por_equipamento(equip)
                except (ValueError, Equipamento.DoesNotExist):
                    self.fields["tipo"].queryset = TipoEquipamento.objects.none()

        apply_tailwind_styles(self)


# ==========================
# Inline Formset (Kit -> ItemKit)
# ==========================
ItemKitFormSet = inlineformset_factory(
    parent_model=Kit,
    model=ItemKit,
    form=ItemKitForm,
    fields=["equipamento", "tipo", "quantidade", "requer_configuracao"],
    extra=1,
    can_delete=True,
)


class TipoEquipamentoForm(forms.ModelForm):
    class Meta:
        model = TipoEquipamento
        fields = ["nome", "ativo"]  # ✅ sem codigo

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_tailwind_styles(self)


TipoEquipamentoFormSet = inlineformset_factory(
    parent_model=Categoria,
    model=TipoEquipamento,
    form=TipoEquipamentoForm,
    fields=["nome", "ativo"],
    extra=0,
    can_delete=True,
)
