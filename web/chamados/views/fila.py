from __future__ import annotations

from django.db.models import Case, IntegerField, Value, When
from django.http import QueryDict
from django.utils import timezone
from django.views.generic import TemplateView
from iam.decorators import user_has_capability
from iam.execucao_capabilities import CAP_EXECUCAO_SESSAO_TOMAR
from iam.mixins import CapabilityRequiredMixin

from chamados.selectors.fila import (
    fila_base_queryset,
    fila_counts,
    fila_projects,
    get_active_sessions_by_chamado,
)
from chamados.selectors.fila_rows import build_fila_rows
from ..models import Chamado


class ChamadoFilaView(CapabilityRequiredMixin, TemplateView):
    template_name = "execucao/fila_operacional.html"
    required_capability = "execucao.chamado.visualizar"

    PRIO_MAP = {
        "CRITICO": Chamado.Prioridade.CRITICA,
        "ALTO": Chamado.Prioridade.ALTA,
        "MEDIO": Chamado.Prioridade.MEDIA,
        "BAIXO": Chamado.Prioridade.BAIXA,
    }

    def _url_with_query(self, **params: object) -> str:
        """
        Monta URL preservando querystring atual e aplicando overrides.
        Para remover um parâmetro, passe None (ex.: projeto=None).
        """
        q = QueryDict(mutable=True)
        q.update(self.request.GET)

        for k, v in params.items():
            if v is None:
                q.pop(k, None)
            else:
                q[k] = str(v)

        encoded = q.urlencode()
        return f"{self.request.path}?{encoded}" if encoded else self.request.path

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        base_qs = fila_base_queryset()
        counts = fila_counts(base_qs)

        prio_key = (self.request.GET.get("prio") or "").strip().upper()
        prio_value = self.PRIO_MAP.get(prio_key)

        raw_projeto = (self.request.GET.get("projeto") or "").strip()
        projeto_id: int | None = None
        if raw_projeto:
            try:
                projeto_id = int(raw_projeto)
            except ValueError:
                projeto_id = None

        qs = base_qs
        if prio_value is not None:
            qs = qs.filter(prioridade=prio_value)

        if projeto_id is not None:
            qs = qs.filter(projeto_id=projeto_id)

        ctx["counts"] = counts
        ctx["prio_selected"] = prio_key if prio_value is not None else None

        ctx["projeto_selected"] = projeto_id
        ctx["projeto_selected_label"] = None
        if projeto_id is not None:
            ctx["projeto_selected_label"] = (
                base_qs.filter(projeto_id=projeto_id)
                .values_list("projeto__nome", flat=True)
                .first()
            )

        ctx["url_clear_prio"] = self._url_with_query(prio=None)
        ctx["url_clear_projeto"] = self._url_with_query(projeto=None)

        ctx["projects_reset_url"] = self._url_with_query(projeto=None)

        ctx["projects"] = fila_projects(
            base_qs,
            projeto_selected=projeto_id,
            url_builder=lambda pid: self._url_with_query(projeto=pid),
        )

        chamados = qs.annotate(
            status_rank=Case(
                When(status=Chamado.Status.EM_EXECUCAO, then=Value(0)),
                When(status=Chamado.Status.ABERTO, then=Value(1)),
                When(status=Chamado.Status.AGUARDANDO_NF, then=Value(2)),
                When(status=Chamado.Status.AGUARDANDO_COLETA, then=Value(3)),
                default=Value(9),
                output_field=IntegerField(),
            ),
            prio_rank=Case(
                When(prioridade=Chamado.Prioridade.CRITICA, then=Value(0)),
                When(prioridade=Chamado.Prioridade.ALTA, then=Value(1)),
                When(prioridade=Chamado.Prioridade.MEDIA, then=Value(2)),
                When(prioridade=Chamado.Prioridade.BAIXA, then=Value(3)),
                When(prioridade=Chamado.Prioridade.PADRAO, then=Value(4)),
                default=Value(4),
                output_field=IntegerField(),
            ),
        ).order_by("status_rank", "prio_rank", "criado_em")

        rows = build_fila_rows(chamados)

        ctx["chamados"] = rows
        ctx["rows"] = rows

        chamado_ids = [r["chamado"].id for r in rows]

        now = timezone.now()
        ctx["execucao_active_sessions_by_chamado"] = get_active_sessions_by_chamado(
            chamado_ids,
            now=now,
        )
        ctx["can_take_session"] = user_has_capability(
            self.request.user,
            CAP_EXECUCAO_SESSAO_TOMAR,
        )
        return ctx
