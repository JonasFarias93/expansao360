from __future__ import annotations

from django.db.models import Count, Q, QuerySet

from ..models import Chamado

FILA_STATUSES = [
    Chamado.Status.ABERTO,
    Chamado.Status.EM_EXECUCAO,
    Chamado.Status.AGUARDANDO_NF,
    Chamado.Status.AGUARDANDO_COLETA,
]


def fila_base_queryset() -> QuerySet[Chamado]:
    return (
        Chamado.objects.filter(status__in=FILA_STATUSES)
        .select_related("loja", "projeto", "subprojeto", "kit")
        .prefetch_related("itens")
    )


def fila_counts(base_qs: QuerySet[Chamado]) -> dict[str, int]:
    return base_qs.aggregate(
        total=Count("id"),
        critico=Count("id", filter=Q(prioridade=Chamado.Prioridade.CRITICA)),
        alto=Count("id", filter=Q(prioridade=Chamado.Prioridade.ALTA)),
        medio=Count("id", filter=Q(prioridade=Chamado.Prioridade.MEDIA)),
        baixo=Count("id", filter=Q(prioridade=Chamado.Prioridade.BAIXA)),
    )
