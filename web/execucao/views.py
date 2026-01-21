# web/execucao/views.py# Create your views here.
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Chamado, InstalacaoItem


def historico(request):
    q = (request.GET.get("q") or "").strip()

    chamados = Chamado.objects.all().order_by("-criado_em")

    if q:
        chamados = chamados.filter(
            Q(protocolo__icontains=q)
            | Q(servicenow_numero__icontains=q)
            | Q(contabilidade_numero__icontains=q)
            | Q(nf_saida_numero__icontains=q)
            | Q(loja__codigo__icontains=q)
            | Q(loja__nome__icontains=q)
            | Q(projeto__codigo__icontains=q)
            | Q(projeto__nome__icontains=q)
            | Q(itens__ativo__icontains=q)
            | Q(itens__numero_serie__icontains=q)
        ).distinct()

    return render(
        request,
        "execucao/historico.html",
        {
            "q": q,
            "chamados": chamados[:200],  # limite simples para não pesar
        },
    )


def chamado_detalhe(request, chamado_id):
    chamado = get_object_or_404(Chamado, pk=chamado_id)
    itens = InstalacaoItem.objects.filter(chamado=chamado).order_by("id")

    return render(
        request,
        "execucao/chamado_detalhe.html",
        {
            "chamado": chamado,
            "itens": itens,
        },
    )


@require_POST
def chamado_finalizar(request, chamado_id):
    chamado = get_object_or_404(Chamado, pk=chamado_id)

    if chamado.finalizado_em:
        messages.warning(request, "Chamado já está finalizado.")
        return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

    try:
        chamado.finalizar()
    except Exception as exc:
        messages.error(request, str(exc))
        return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

    messages.success(request, "Chamado finalizado com sucesso.")
    return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)
