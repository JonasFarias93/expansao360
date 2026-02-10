# web/execucao/forms.py
from __future__ import annotations

from cadastro.models import Kit, Loja, Projeto, Subprojeto
from django import forms
from django.core.exceptions import ValidationError
from django.urls import reverse

from execucao.models import NF_SAIDA_ONLY_DIGITS_ERROR, Chamado


class ChamadoCreateForm(forms.Form):
    loja = forms.ModelChoiceField(
        queryset=Loja.objects.order_by("codigo"),
        required=True,
        label="Loja",
        error_messages={
            "required": "Informe um código de loja válido.",
            "invalid_choice": "Loja não encontrada.",
        },
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

    # ✅ Ticket Externo (obrigatório)
    ticket_externo_sistema = forms.CharField(
        required=True,
        max_length=50,
        label="Sistema do ticket externo",
        help_text="Ex.: ServiceNow, Jira, GLPI…",
    )
    ticket_externo_id = forms.CharField(
        required=True,
        max_length=50,
        label="Número do ticket externo",
    )

    # ✅ Prioridade (opcional, default MAIS_ANTIGO no model)
    prioridade = forms.ChoiceField(
        required=False,
        choices=Chamado.Prioridade.choices,
        label="Prioridade",
        help_text="Se não informar, entra como Mais antigo (padrão).",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        base = (
            "w-full rounded-lg border border-slate-300 px-3 py-2 "
            "focus:outline-none focus:ring-2 focus:ring-slate-900"
        )
        for _name, field in self.fields.items():
            current = (field.widget.attrs.get("class") or "").strip()
            field.widget.attrs["class"] = f"{current} {base}".strip() if current else base

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

    def clean(self):
        cleaned = super().clean()

        # ------------------------------
        # Ticket externo (trim + required)
        # ------------------------------
        sistema = (cleaned.get("ticket_externo_sistema") or "").strip()
        ticket_id = (cleaned.get("ticket_externo_id") or "").strip()

        if not sistema:
            self.add_error("ticket_externo_sistema", "Campo obrigatório.")
        if not ticket_id:
            self.add_error("ticket_externo_id", "Campo obrigatório.")

        cleaned["ticket_externo_sistema"] = sistema
        cleaned["ticket_externo_id"] = ticket_id

        # ------------------------------
        # Loja (backstop server-side)
        # ------------------------------
        # UI nova envia:
        # - loja_codigo (texto digitado)
        # - loja (hidden) com ID real do ModelChoiceField
        loja = cleaned.get("loja")

        if loja is None:
            # Mantém mensagem coerente com o novo fluxo (por código)
            self.add_error("loja", "Informe um código de loja válido.")
            return cleaned

        # Garantia extra contra injeção/edge-cases (intenção explícita)
        if not Loja.objects.filter(id=loja.id).exists():
            raise ValidationError("Loja não encontrada.")

        return cleaned


class ChamadoDadosFiscaisForm(forms.ModelForm):
    class Meta:
        model = Chamado
        fields = ["contabilidade_numero", "nf_saida_numero"]

    def clean_contabilidade_numero(self) -> str | None:
        v = self.cleaned_data.get("contabilidade_numero")
        if v is None:
            return v
        return v.strip()

    def clean_nf_saida_numero(self) -> str | None:
        v = self.cleaned_data.get("nf_saida_numero")
        if v is None:
            return v
        v = "".join(v.split())
        if v and not v.isdigit():
            raise forms.ValidationError(NF_SAIDA_ONLY_DIGITS_ERROR)
        return v
