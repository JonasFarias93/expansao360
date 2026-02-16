from __future__ import annotations

from cadastro.models import Projeto
from django.db.models import Case, Count, IntegerField, Value, When
from django.http import QueryDict
from django.utils import timezone
from django.views.generic import TemplateView
from execucao.models import ExecutionSession
from iam.decorators import user_has_capability
from iam.execucao_capabilities import CAP_EXECUCAO_SESSAO_TOMAR
from iam.mixins import CapabilityRequiredMixin
from chamados.selectors.fila import fila_base_queryset, fila_counts
from ..models import Chamado, StatusConfiguracao


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
                    "url": self._url_with_query(projeto=pid),
                    "active": projeto_id == pid,
                }
            )

        ctx["projects"] = projects

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

        rows: list[dict[str, object]] = []
        for ch in chamados:
            itens = list(ch.itens.all())
            rastreaveis = [i for i in itens if i.tem_ativo]
            contaveis = [i for i in itens if not i.tem_ativo]
            cfg = [i for i in itens if i.deve_configurar]

            bipados = sum(
                1
                for i in rastreaveis
                if (i.ativo or "").strip() and (i.numero_serie or "").strip()
            )
            checados = sum(1 for i in contaveis if i.confirmado)
            cfg_done = sum(
                1
                for i in cfg
                if i.status_configuracao == StatusConfiguracao.CONFIGURADO and i.ip
            )

            rows.append(
                {
                    "chamado": ch,
                    "pode_liberar_nf": ch.pode_liberar_nf(),
                    "bipados": bipados,
                    "bip_total": len(rastreaveis),
                    "checados": checados,
                    "check_total": len(contaveis),
                    "cfg_done": cfg_done,
                    "cfg_total": len(cfg),
                }
            )

        ctx["chamados"] = rows
        ctx["rows"] = rows

        chamado_ids = [r["chamado"].id for r in rows]

        active_sessions_by_chamado: dict[int, ExecutionSession] = {}
        if chamado_ids:
            now = timezone.now()
            qs_sessions = (
                ExecutionSession.objects.filter(
                    chamado_id__in=chamado_ids,
                    ended_at__isnull=True,
                    expires_at__gt=now,
                )
                .select_related("usuario")
                .order_by("chamado_id", "-started_at")
            )

            for s in qs_sessions:
                if s.chamado_id not in active_sessions_by_chamado:
                    active_sessions_by_chamado[s.chamado_id] = s

        ctx["execucao_active_sessions_by_chamado"] = active_sessions_by_chamado
        ctx["can_take_session"] = user_has_capability(
            self.request.user,
            CAP_EXECUCAO_SESSAO_TOMAR,
        )
        return ctx
