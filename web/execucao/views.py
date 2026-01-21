# web/execucao/views.py# Create your views here.
from django.db.models import Q
from django.shortcuts import render

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
