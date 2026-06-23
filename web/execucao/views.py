# web/execucao/views.py
from __future__ import annotations

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Case, Count, IntegerField, Q, Value, When
from django.http import HttpResponseBadRequest, QueryDict
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from cadastro.models import Projeto
from chamados.models import StatusConfiguracao
from iam.decorators import user_has_capability
from iam.execucao_capabilities import (
    CAP_EXECUCAO_CHAMADO_EDITAR,
    CAP_EXECUCAO_SESSAO_TOMAR,
)
from iam.mixins import CapabilityRequiredMixin

from execucao.services.execution_session import (
    NoActiveSessionToTakeError,
    take_session,
)
from execucao.services.open_session import SessionBlockedError, open_session

from .models import (
    Chamado,
    ExecutionSession,
)


@login_required
@require_POST
def chamado_abrir(request, chamado_id: int):
    if not user_has_capability(request.user, CAP_EXECUCAO_CHAMADO_EDITAR):
        raise PermissionDenied

    chamado = get_object_or_404(Chamado, pk=chamado_id)

    try:
        open_session(chamado=chamado, user=request.user)
    except SessionBlockedError:
        from execucao.services.execution_session import get_active_session

        active = get_active_session(chamado=chamado)
        if active is not None:
            messages.error(
                request,
                (
                    f"Chamado em execução por {active.usuario} "
                    f"desde {active.started_at:%d/%m/%Y %H:%M}."
                ),
            )
        else:
            messages.error(request, "Chamado em execução por outro usuário.")

        return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

    # Direciona para a tela “editável” correta
    if chamado.status == Chamado.Status.ABERTO:
        return redirect("execucao:chamado_setup", chamado_id=chamado.id)

    return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)


@login_required
@require_POST
def chamado_take_session(request, chamado_id: int):
    chamado = get_object_or_404(Chamado, pk=chamado_id)

    # Permissão é enforced no serviço (IAM como autoridade).
    # Se preferir “perm primeiro” como no abrir, dá pra checar aqui também,
    # mas manter no serviço evita duplicação.
    try:
        take_session(chamado=chamado, actor=request.user)
    except NoActiveSessionToTakeError:
        return HttpResponseBadRequest("Não há sessão ativa para tomar.")

    messages.success(
        request,
        "Sessão tomada com sucesso. Você está editando este chamado.",
    )

    # Direciona para a tela “editável” correta (mesmo fluxo do abrir)
    if chamado.status == Chamado.Status.ABERTO:
        return redirect("execucao:chamado_setup", chamado_id=chamado.id)

    return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)


# ================
# sessao:fila_operacional
# (movida de chamados/views.py — checklist item 3.1)
# ================
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

        base_qs = (
            Chamado.objects.filter(status__in=[
                Chamado.Status.ABERTO,
                Chamado.Status.EM_EXECUCAO,
                Chamado.Status.AGUARDANDO_NF,
                Chamado.Status.AGUARDANDO_COLETA,
            ])
            .select_related("loja", "projeto", "subprojeto", "kit")
            .prefetch_related("itens")
        )

        counts = base_qs.aggregate(
            total=Count("id"),
            critico=Count("id", filter=Q(prioridade=Chamado.Prioridade.CRITICA)),
            alto=Count("id", filter=Q(prioridade=Chamado.Prioridade.ALTA)),
            medio=Count("id", filter=Q(prioridade=Chamado.Prioridade.MEDIA)),
            baixo=Count("id", filter=Q(prioridade=Chamado.Prioridade.BAIXA)),
        )

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
                .values_list("projeto__nome", flat=True).first()
            )

        ctx["url_clear_prio"] = self._url_with_query(prio=None)
        ctx["url_clear_projeto"] = self._url_with_query(projeto=None)
        ctx["projects_reset_url"] = self._url_with_query(projeto=None)

        proj_rows = base_qs.values("projeto_id").annotate(count=Count("id")).order_by("-count")
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
            projects.append({
                "id": pid,
                "projeto": proj,
                "nome": proj.nome,
                "count": r["count"],
                "url": self._url_with_query(projeto=pid),
                "active": projeto_id == pid,
            })
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
            bipados = sum(1 for i in rastreaveis if (i.ativo or "").strip() and (i.numero_serie or "").strip())
            checados = sum(1 for i in contaveis if i.confirmado)
            cfg_done = sum(1 for i in cfg if i.status_configuracao == StatusConfiguracao.CONFIGURADO and i.ip)
            rows.append({
                "chamado": ch,
                "pode_liberar_nf": ch.pode_liberar_nf(),
                "bipados": bipados,
                "bip_total": len(rastreaveis),
                "checados": checados,
                "check_total": len(contaveis),
                "cfg_done": cfg_done,
                "cfg_total": len(cfg),
            })

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
        ctx["can_take_session"] = user_has_capability(self.request.user, CAP_EXECUCAO_SESSAO_TOMAR)
        return ctx