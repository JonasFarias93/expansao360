from cadastro.models import Kit, Loja, Projeto, Subprojeto
from django import forms
from django.urls import reverse


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
        queryset=Subprojeto.objects.none(),
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

        # Descobre projeto_id (POST / GET com params / initial)
        projeto_id = None
        if self.is_bound:
            projeto_id = self.data.get("projeto") or None
        else:
            initial_projeto = self.initial.get("projeto")
            if initial_projeto:
                projeto_id = getattr(initial_projeto, "pk", initial_projeto)

        # Ajusta queryset quando já existe projeto_id (POST ou initial)
        if projeto_id:
            self.fields["subprojeto"].queryset = Subprojeto.objects.filter(
                projeto_id=projeto_id
            ).order_by("codigo")
        else:
            self.fields["subprojeto"].queryset = Subprojeto.objects.none()

        self.fields["subprojeto"].help_text = "Selecione o subprojeto do projeto escolhido."

        # HTMX: carrega subprojetos ao mudar projeto E também ao carregar a página
        self.fields["projeto"].widget.attrs.update(
            {
                "hx-get": reverse("execucao:ajax_subprojetos"),
                "hx-trigger": "load, change",
                "hx-target": "#id_subprojeto",
                "hx-swap": "innerHTML",
                "hx-include": "[name='projeto']",
            }
        )
