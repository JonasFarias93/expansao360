# web/execucao/views.py# Create your views here.
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Chamado


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
    chamado = get_object_or_404(
        Chamado.objects.select_related("loja", "projeto", "subprojeto", "kit"),
        pk=chamado_id,
    )
    itens = list(chamado.itens.select_related("equipamento").all().order_by("id"))

    return render(
        request,
        "execucao/chamado_detalhe.html",
        {"chamado": chamado, "itens": itens},
    )


@require_POST
@transaction.atomic
def chamado_atualizar_itens(request, chamado_id):
    chamado = get_object_or_404(Chamado, pk=chamado_id)

    if chamado.status == Chamado.Status.FINALIZADO:
        messages.warning(request, "Chamado já está finalizado. Não é possível editar itens.")
        return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

    itens = list(chamado.itens.select_related("equipamento").all())

    for item in itens:
        if item.tem_ativo:
            item.ativo = (request.POST.get(f"ativo_{item.id}") or "").strip()
            item.numero_serie = (request.POST.get(f"serie_{item.id}") or "").strip()
        else:
            item.confirmado = request.POST.get(f"confirmado_{item.id}") == "on"

        item.save(update_fields=["ativo", "numero_serie", "confirmado"])

    if chamado.status == Chamado.Status.ABERTO:
        chamado.status = Chamado.Status.EM_EXECUCAO
        chamado.save(update_fields=["status"])

    messages.success(request, "Itens atualizados com sucesso.")
    return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)


@require_POST
def chamado_finalizar(request, chamado_id):
    chamado = get_object_or_404(Chamado, pk=chamado_id)

    try:
        chamado.finalizar()
    except ValidationError as exc:
        # exc pode ser lista, dict ou string — normalize para messages
        if hasattr(exc, "messages"):
            for msg in exc.messages:
                messages.error(request, msg)
        else:
            messages.error(request, str(exc))
        return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

    messages.success(request, "Chamado finalizado com sucesso.")
    return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)
