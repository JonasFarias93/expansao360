from __future__ import annotations
from collections.abc import Callable
from django.db.models import Count, Q, QuerySet

from collections.abc import Iterable

from execucao.models import ExecutionSession
from cadastro.models import Projeto
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


def fila_projects(
    base_qs: QuerySet[Chamado],
    *,
    projeto_selected: int | None,
    url_builder: Callable[[int], str],
) -> list[dict[str, object]]:
    """
    Monta a lista de projetos usada no bloco lateral da fila.

    - Ordena por quantidade de chamados na fila (desc)
    - Marca o projeto ativo conforme `projeto_selected`
    - Gera URL via `url_builder(pid)` (sem acoplar em request/view)
    """
    proj_rows = (
        base_qs.values("projeto_id").annotate(count=Count("id")).order_by("-count")
    )

    proj_ids = [r["projeto_id"] for r in proj_rows if r["projeto_id"] is not None]
    proj_map = Projeto.objects.in_bulk(proj_ids)

    projects: list[dict[str, object]] = []
    for r in proj_rows:
        pid = r["projeto_id"]
        if pid is None:
            continue

        proj = proj_map.get(pid)
        if not proj:
            continue

        projects.append(
            {
                "id": pid,
                "projeto": proj,
                "nome": proj.nome,
                "count": r["count"],
                "url": url_builder(pid),
                "active": projeto_selected == pid,
            }
        )

    return projects


def get_active_sessions_by_chamado(
    chamado_ids: Iterable[int],
    *,
    now,
) -> dict[int, ExecutionSession]:
    """
    Retorna a sessão ativa mais recente por chamado.

    Regra de "ativa":
    - ended_at IS NULL
    - expires_at > now

    Mais recente:
    - maior started_at (desc)
    """
    ids = [int(i) for i in chamado_ids if i is not None]
    if not ids:
        return {}

    qs = (
        ExecutionSession.objects.filter(
            chamado_id__in=ids,
            ended_at__isnull=True,
            expires_at__gt=now,
        )
        .select_related("usuario")
        .order_by("chamado_id", "-started_at")
    )

    out: dict[int, ExecutionSession] = {}
    for s in qs:
        if s.chamado_id not in out:
            out[s.chamado_id] = s
    return out
