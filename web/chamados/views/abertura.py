from __future__ import annotations

from cadastro.models import Subprojeto
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.html import escape
from django.views import View
from iam.mixins import CapabilityRequiredMixin

from ..forms import ChamadoCreateForm
from ..models import Chamado
from .workflow import _push_validation_error_messages


@login_required
def subprojetos_por_projeto(request: HttpRequest) -> HttpResponse:
    projeto_id = (request.GET.get("projeto") or "").strip()

    options = ['<option value="">---------</option>']

    if not projeto_id.isdigit():
        return HttpResponse("".join(options))

    qs = Subprojeto.objects.filter(projeto_id=projeto_id).order_by("codigo")

    for sp in qs:
        options.append(f'<option value="{sp.pk}">{escape(str(sp))}</option>')

    return HttpResponse("".join(options))


class ChamadoCreateView(CapabilityRequiredMixin, View):
    required_capability = "execucao.chamado.criar"
    template_name = "execucao/chamado_abertura.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        form = ChamadoCreateForm()
        return render(request, self.template_name, {"form": form})

    @transaction.atomic
    def post(self, request: HttpRequest) -> HttpResponse:
        form = ChamadoCreateForm(request.POST)

        if not form.is_valid():
            return render(request, self.template_name, {"form": form})

        prioridade = form.cleaned_data.get("prioridade") or Chamado.Prioridade.PADRAO

        chamado = Chamado(
            loja=form.cleaned_data["loja"],
            projeto=form.cleaned_data["projeto"],
            subprojeto=form.cleaned_data["subprojeto"],
            kit=form.cleaned_data["kit"],
            status=Chamado.Status.EM_ABERTURA,
            tipo=Chamado.Tipo.ENVIO,
            ticket_externo_sistema=(
                form.cleaned_data.get("ticket_externo_sistema") or ""
            ).strip(),
            ticket_externo_id=(
                form.cleaned_data.get("ticket_externo_id") or ""
            ).strip(),
            prioridade=prioridade,
        )

        try:
            chamado.full_clean()
        except ValidationError as exc:
            _push_validation_error_messages(request, exc)
            return render(request, self.template_name, {"form": form})

        chamado.save()

        chamado.gerar_itens_de_instalacao()

        messages.success(
            request,
            f"Chamado {chamado.protocolo} criado. Complete o setup para entrar na fila.",
        )
        return redirect("execucao:chamado_setup", chamado_id=chamado.id)
