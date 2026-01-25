# web/cadastro/forms.py
from django import forms
from django.forms import inlineformset_factory

from .models import Categoria, Equipamento, ItemKit, Kit, Loja, Projeto, Subprojeto

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
    class Meta:
        model = Loja
        fields = ["codigo", "nome"]

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


# ==========================
# Inline Formset (Kit -> ItemKit)
# ==========================
ItemKitFormSet = inlineformset_factory(
    parent_model=Kit,
    model=ItemKit,
    fields=["equipamento", "tipo", "quantidade", "requer_configuracao"],
    extra=1,
    can_delete=True,
)
