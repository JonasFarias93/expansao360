# web/execucao/forms.py
from cadastro.models import Kit, Loja, Projeto, Subprojeto
from django import forms


class ChamadoCreateForm(forms.Form):
    loja = forms.ModelChoiceField(
        queryset=Loja.objects.order_by("codigo"),
        required=True,
        label="Loja",
    )
    projeto = forms.ModelChoiceField(
        queryset=Projeto.objects.order_by("codigo"),
        required=True,
        label="Projeto",
    )
    subprojeto = forms.ModelChoiceField(
        queryset=Subprojeto.objects.select_related("projeto").order_by("projeto__codigo", "codigo"),
        required=True,
        label="Subprojeto",
    )
    kit = forms.ModelChoiceField(
        queryset=Kit.objects.order_by("nome"),
        required=True,
        label="Kit",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        base = (
            "w-full rounded-lg border border-slate-300 px-3 py-2 "
            "focus:outline-none focus:ring-2 focus:ring-slate-900"
        )

        for _name, field in self.fields.items():
            field.widget.attrs["class"] = base

        # placeholders leves
        self.fields["subprojeto"].help_text = "Selecione o subprojeto (obrigatório por enquanto)."
