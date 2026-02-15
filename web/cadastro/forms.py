# web/cadastro/forms.py
from __future__ import annotations

from django import forms
from django.db.models import Q
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

        if isinstance(widget, forms.HiddenInput):
            continue

        if isinstance(widget, forms.CheckboxInput):
            widget.attrs["class"] = BASE_CHECKBOX_CSS
            continue

        # ✅ isinstance precisa de type ou tuple[types]
        if isinstance(widget, (forms.Select, forms.SelectMultiple)):  # noqa: UP038
            widget.attrs["class"] = BASE_SELECT_CSS
            continue

        # default: text/number/etc
        widget.attrs["class"] = BASE_INPUT_CSS


# ==========================
# Forms
# ==========================
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nome", "disponivel"]
        labels = {
            "nome": "Nome",
            "disponivel": "Disponível",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_tailwind_styles(self)


class LojaForm(forms.ModelForm):
    """
    Loja.codigo = Java (business_key legado). Continua editável e obrigatório no fluxo.
    """

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
    """
    Projeto.codigo é gerado automaticamente (PRO-{seq}), então não aparece no form.
    """

    class Meta:
        model = Projeto
        fields = ["nome", "cor_slug"]
        labels = {
            "nome": "Nome",
            "cor_slug": "Cor do projeto",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_tailwind_styles(self)


class SubprojetoForm(forms.ModelForm):
    """
    Subprojeto.codigo é gerado automaticamente (SUB-{seq}), então não aparece no form.
    """

    class Meta:
        model = Subprojeto
        fields = ["projeto", "nome"]
        labels = {
            "projeto": "Projeto",
            "nome": "Nome",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # UX: ordenar projetos no select
        self.fields["projeto"].queryset = Projeto.objects.order_by("codigo", "nome")
        apply_tailwind_styles(self)


class EquipamentoForm(forms.ModelForm):
    """
    Equipamento.codigo é gerado automaticamente (EQP-{seq}), então não aparece no form.
    """

    class Meta:
        model = Equipamento
        fields = ["nome", "categoria", "tem_ativo", "configuravel"]
        labels = {
            "nome": "Nome",
            "categoria": "Categoria",
            "tem_ativo": "Tem ativo",
            "configuravel": "Configurável",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # UX: ordenar categorias no select
        self.fields["categoria"].queryset = Categoria.objects.order_by("nome")
        apply_tailwind_styles(self)


class KitForm(forms.ModelForm):
    class Meta:
        model = Kit
        fields = ["nome"]
        labels = {"nome": "Nome"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_tailwind_styles(self)


class ItemKitForm(forms.ModelForm):
    class Meta:
        model = ItemKit
        fields = ["equipamento", "tipo", "quantidade", "requer_configuracao"]
        labels = {
            "equipamento": "Equipamento",
            "tipo": "Tipo",
            "quantidade": "Quantidade",
            "requer_configuracao": "Requer configuração",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # HTMX: ao trocar equipamento, atualizar opções de tipo (por categoria do equipamento)
        self.fields["equipamento"].widget.attrs.update(
            {
                "hx-get": reverse_lazy("registry:ajax_tipos_por_equipamento"),
                "hx-trigger": "change",
                "hx-target": f"#id_{self.prefix}-tipo" if self.prefix else "#id_tipo",
                "hx-swap": "innerHTML",
            }
        )

        # default: vazio (evita escolher tipo errado antes de selecionar equipamento)
        self.fields["tipo"].queryset = TipoEquipamento.objects.none()

        def _set_tipos_por_categoria_id(categoria_id: int | None) -> None:
            """
            Popula o select de tipos a partir da categoria.
            BLINDAGEM: inclui o tipo atual da instância mesmo se indisponível
            (evita "---------" ao editar itens antigos).
            """
            if not categoria_id:
                self.fields["tipo"].queryset = TipoEquipamento.objects.none()
                return

            tipo_atual_id = getattr(self.instance, "tipo_id", None)

            qs = TipoEquipamento.objects.filter(categoria_id=categoria_id)
            if tipo_atual_id:
                qs = qs.filter(Q(disponivel=True) | Q(id=tipo_atual_id))
            else:
                qs = qs.filter(disponivel=True)

            self.fields["tipo"].queryset = qs.order_by("nome")

        def _set_tipos_por_equipamento(equip: Equipamento | None) -> None:
            """
            TipoEquipamento pertence a Categoria -> filtra por equipamento.categoria.
            """
            if not equip or not getattr(equip, "categoria_id", None):
                _set_tipos_por_categoria_id(None)
                return
            _set_tipos_por_categoria_id(equip.categoria_id)

        # ----------------------------
        # Caso 1: edição (GET) - instance existente
        # Garante queryset do tipo populado e valor selecionado aparecer no select.
        # ----------------------------
        if getattr(self.instance, "pk", None) and getattr(
            self.instance, "equipamento_id", None
        ):
            equipamento = getattr(self.instance, "equipamento", None)

            if equipamento is not None and getattr(equipamento, "categoria_id", None):
                _set_tipos_por_equipamento(equipamento)
            else:
                # fallback barato: pega apenas categoria_id do equipamento
                categoria_id = (
                    Equipamento.objects.filter(id=self.instance.equipamento_id)
                    .values_list("categoria_id", flat=True)
                    .first()
                )
                _set_tipos_por_categoria_id(int(categoria_id) if categoria_id else None)

        # ----------------------------
        # Caso 2: POST (form bound) - usuário selecionou equipamento no form
        # ----------------------------
        if self.data:
            equipamento_key = (
                f"{self.prefix}-equipamento" if self.prefix else "equipamento"
            )
            equip_id = self.data.get(equipamento_key)

            if equip_id:
                try:
                    equip = Equipamento.objects.select_related("categoria").get(
                        id=int(equip_id)
                    )
                    _set_tipos_por_equipamento(equip)
                except (ValueError, Equipamento.DoesNotExist):
                    _set_tipos_por_categoria_id(None)

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
    """
    TipoEquipamento.codigo é semântico e gerado pelo model quando vazio.
    Não expomos codigo no form (governança).
    """

    class Meta:
        model = TipoEquipamento
        fields = ["nome", "disponivel"]
        labels = {
            "nome": "Nome",
            "disponivel": "Disponível",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_tailwind_styles(self)


TipoEquipamentoFormSet = inlineformset_factory(
    parent_model=Categoria,
    model=TipoEquipamento,
    form=TipoEquipamentoForm,
    fields=["nome", "disponivel"],
    extra=0,
    can_delete=True,
)
