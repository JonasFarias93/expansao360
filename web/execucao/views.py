# web/execucao/views.py
from __future__ import annotations

from cadastro.models import Subprojeto
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Case, Count, IntegerField, Q, Value, When
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import TemplateView
from iam.mixins import CapabilityRequiredMixin

from .forms import ChamadoCreateForm
from .models import (
    Chamado,
    EvidenciaChamado,
    InstalacaoItem,
    ItemConfiguracaoLog,
    StatusConfiguracao,
)


def _push_validation_error_messages(request: HttpRequest, exc: ValidationError) -> None:
    """
    Normaliza ValidationError para mensagens no Django messages framework.
    - ValidationError pode vir com .messages (lista)
    - ou .message_dict (dict campo -> lista msgs)
    """
    if hasattr(exc, "message_dict") and getattr(exc, "message_dict", None):
        for _field, msgs in exc.message_dict.items():  # type: ignore[attr-defined]
            for msg in msgs:
                messages.error(request, msg)
        return

    for msg in getattr(exc, "messages", [str(exc)]):
        messages.error(request, msg)


# ============================
# AJAX: SUBPROJETOS POR PROJETO
# ============================
@login_required
def subprojetos_por_projeto(request: HttpRequest) -> HttpResponse:
    """
    Retorna as <option> para o select de subprojeto filtrado por projeto.

    Querystring:
      ?projeto=<id>

    Resposta:
      HTML com opções (<option>...</option>)
    """
    projeto_id = (request.GET.get("projeto") or "").strip()

    # Sempre devolve a opção vazia padrão.
    options = ['<option value="">---------</option>']

    if not projeto_id.isdigit():
        return HttpResponse("".join(options))

    qs = Subprojeto.objects.filter(projeto_id=projeto_id).order_by("codigo")

    # Usa __str__ do Subprojeto (idealmente: "CODIGO - NOME")
    for sp in qs:
        options.append(f'<option value="{sp.pk}">{escape(str(sp))}</option>')

    return HttpResponse("".join(options))


# ==================
# CHAMADO (ABERTURA)
# ==================
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
            # 🔥 NOVO FLUXO:
            # Após tela 1, o chamado fica em EM_ABERTURA (setup),
            # e só vira ABERTO após "Salvar setup".
            status=Chamado.Status.EM_ABERTURA,
            tipo=Chamado.Tipo.ENVIO,
            ticket_externo_sistema=(form.cleaned_data.get("ticket_externo_sistema") or "").strip(),
            ticket_externo_id=(form.cleaned_data.get("ticket_externo_id") or "").strip(),
            prioridade=prioridade,
        )

        try:
            chamado.full_clean()
        except ValidationError as exc:
            _push_validation_error_messages(request, exc)
            return render(request, self.template_name, {"form": form})

        chamado.save()

        # Deve ser idempotente (não pode duplicar itens)
        chamado.gerar_itens_de_instalacao()

        messages.success(
            request,
            f"Chamado {chamado.protocolo} criado. Complete o setup para entrar na fila.",
        )
        return redirect("execucao:chamado_setup", chamado_id=chamado.id)


# ==================
# CHAMADO (SETUP)
# ==================
@method_decorator(ensure_csrf_cookie, name="dispatch")
class ChamadoSetupView(CapabilityRequiredMixin, View):
    """
    Tela 2 do fluxo: Setup/Planejamento.
    - Permite marcar deve_configurar e capturar IP quando necessário.
    - Não é execução operacional.
    """

    required_capability = "execucao.chamado.criar"
    template_name = "execucao/chamado_setup.html"

    def get(self, request: HttpRequest, chamado_id: int) -> HttpResponse:
        chamado = get_object_or_404(
            Chamado.objects.select_related("loja", "projeto", "subprojeto", "kit"),
            pk=chamado_id,
        )

        # Setup só faz sentido quando ainda está em EM_ABERTURA.
        # Se já estiver ABERTO+, manda para a execução.
        if chamado.status != Chamado.Status.EM_ABERTURA:
            return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

        chamado.gerar_itens_de_instalacao()
        itens_qs = chamado.itens.select_related("equipamento").all().order_by("id")

        motivos_bloqueio: list[str] = []
        for item in itens_qs:
            if not item.equipamento.configuravel:
                continue
            if not item.deve_configurar:
                continue
            if not (item.ip or "").strip():
                motivos_bloqueio.append(
                    f"Item '{item.equipamento.nome}': informe o IP (configuração marcada).",
                )

        config_total = itens_qs.filter(deve_configurar=True).count()
        config_done = (
            itens_qs.filter(
                deve_configurar=True,
                status_configuracao=StatusConfiguracao.CONFIGURADO,
            )
            .exclude(ip__isnull=True)
            .exclude(ip="")
            .count()
        )
        config_pct = int((config_done * 100) / config_total) if config_total else 0

        context = {
            "chamado": chamado,
            "itens": list(itens_qs),
            "config_total": config_total,
            "config_done": config_done,
            "config_pct": config_pct,
            "motivos_bloqueio": motivos_bloqueio,
            "is_setup": True,
        }

        return render(request, self.template_name, context)


# ==================
# FILA (HOME)
# ==================
class ChamadoFilaView(CapabilityRequiredMixin, TemplateView):
    """
    Fila operacional de chamados ativos.
    """

    template_name = "execucao/fila_operacional.html"
    required_capability = "execucao.chamado.visualizar"

    # URL -> Enum do model
    PRIO_MAP = {
        "CRITICO": Chamado.Prioridade.CRITICA,
        "ALTO": Chamado.Prioridade.ALTA,
        "MEDIO": Chamado.Prioridade.MEDIA,
        "BAIXO": Chamado.Prioridade.BAIXA,
    }

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # 1) queryset base da fila (sem filtro de prioridade)
        base_qs = (
            Chamado.objects.filter(
                status__in=[
                    Chamado.Status.ABERTO,
                    Chamado.Status.EM_EXECUCAO,
                    Chamado.Status.AGUARDANDO_NF,
                    Chamado.Status.AGUARDANDO_COLETA,
                ]
            )
            .select_related("loja", "projeto", "subprojeto", "kit")
            .prefetch_related("itens")
        )

        # 2) counts (sempre do conjunto "fila", independente do filtro)
        counts = base_qs.aggregate(
            total=Count("id"),
            critico=Count("id", filter=Q(prioridade=Chamado.Prioridade.CRITICA)),
            alto=Count("id", filter=Q(prioridade=Chamado.Prioridade.ALTA)),
            medio=Count("id", filter=Q(prioridade=Chamado.Prioridade.MEDIA)),
            baixo=Count("id", filter=Q(prioridade=Chamado.Prioridade.BAIXA)),
        )

        # 3) filtro por prioridade (stateless via querystring)
        prio_key = (self.request.GET.get("prio") or "").strip().upper()
        prio_value = self.PRIO_MAP.get(prio_key)  # Enum ou None

        qs = base_qs
        if prio_value is not None:
            qs = qs.filter(prioridade=prio_value)

        # 4) ordenação/annotate (aplicar depois do filtro)
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

        # 5) montar rows (e expor rows como "chamados" pro template atual)
        rows: list[dict[str, object]] = []
        for ch in chamados:
            itens = list(ch.itens.all())
            rastreaveis = [i for i in itens if i.tem_ativo]
            contaveis = [i for i in itens if not i.tem_ativo]
            cfg = [i for i in itens if i.deve_configurar]

            bipados = sum(
                1 for i in rastreaveis if (i.ativo or "").strip() and (i.numero_serie or "").strip()
            )
            checados = sum(1 for i in contaveis if i.confirmado)
            cfg_done = sum(
                1 for i in cfg if i.status_configuracao == StatusConfiguracao.CONFIGURADO and i.ip
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

        ctx["counts"] = counts
        ctx["prio_selected"] = prio_key if prio_value is not None else None

        # importante: manter compat com seu template atual
        ctx["chamados"] = rows
        ctx["rows"] = rows
        return ctx


# ==================
# HISTÓRICO
# ==================
class HistoricoView(CapabilityRequiredMixin, TemplateView):
    template_name = "execucao/historico_chamados.html"
    required_capability = "execucao.chamado.visualizar"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        q = (self.request.GET.get("q") or "").strip()

        chamados = Chamado.objects.all().select_related("loja", "projeto").order_by("-criado_em")

        if q:
            chamados = chamados.filter(
                Q(protocolo__icontains=q)
                | Q(ticket_externo_id__icontains=q)
                | Q(ticket_externo_sistema__icontains=q)
                | Q(servicenow_numero__icontains=q)  # legado
                | Q(contabilidade_numero__icontains=q)
                | Q(nf_saida_numero__icontains=q)
                | Q(loja__codigo__icontains=q)
                | Q(loja__nome__icontains=q)
                | Q(projeto__codigo__icontains=q)
                | Q(projeto__nome__icontains=q)
                | Q(itens__ativo__icontains=q)
                | Q(itens__numero_serie__icontains=q)
            ).distinct()

        ctx["q"] = q
        ctx["chamados"] = chamados[:200]
        return ctx


# ==================
# CHAMADO (EXECUÇÃO)
# ==================
class ChamadoExecucaoView(CapabilityRequiredMixin, TemplateView):
    template_name = "execucao/chamado_execucao.html"
    required_capability = "execucao.chamado.visualizar"

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        chamado_id = kwargs["chamado_id"]
        chamado = get_object_or_404(Chamado, pk=chamado_id)

        # Detalhe/execução não é permitido quando ainda está em EM_ABERTURA.
        if chamado.status == Chamado.Status.EM_ABERTURA:
            return redirect("execucao:chamado_setup", chamado_id=chamado.id)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        chamado_id = kwargs["chamado_id"]

        chamado = get_object_or_404(
            Chamado.objects.select_related("loja", "projeto", "subprojeto", "kit"),
            pk=chamado_id,
        )

        chamado.gerar_itens_de_instalacao()

        itens_qs = chamado.itens.select_related("equipamento").all().order_by("id")

        config_total = itens_qs.filter(deve_configurar=True).count()
        config_done = (
            itens_qs.filter(
                deve_configurar=True,
                status_configuracao=StatusConfiguracao.CONFIGURADO,
            )
            .exclude(ip__isnull=True)
            .exclude(ip="")
            .count()
        )
        config_pct = int((config_done * 100) / config_total) if config_total else 0

        evidencias = EvidenciaChamado.objects.filter(chamado=chamado).order_by("-criado_em", "-id")
        evidencia_tipos = list(EvidenciaChamado.Tipo.choices)

        is_envio = chamado.tipo == Chamado.Tipo.ENVIO
        is_retorno = chamado.tipo == Chamado.Tipo.RETORNO
        gate_contabil_ok = bool((chamado.contabilidade_numero or "").strip())
        gate_nf_ok = bool((chamado.nf_saida_numero or "").strip())
        gate_coleta_ok = chamado.coleta_confirmada_em is not None

        ctx.update(
            {
                "chamado": chamado,
                "itens": list(itens_qs),
                "evidencias": evidencias,
                "evidencia_tipos": evidencia_tipos,
                "config_total": config_total,
                "config_done": config_done,
                "config_pct": config_pct,
                "pode_liberar_nf": chamado.pode_liberar_nf(),
                "is_envio": is_envio,
                "is_retorno": is_retorno,
                "gate_contabil_ok": gate_contabil_ok,
                "gate_nf_ok": gate_nf_ok,
                "gate_coleta_ok": gate_coleta_ok,
                "is_setup": False,
            }
        )
        return ctx


# ==========================
# CHAMADO: ADMIN / WORKFLOW
# ==========================
class ChamadoInformarContabilView(CapabilityRequiredMixin, View):
    required_capability = "execucao.chamado.editar_referencias"

    @transaction.atomic
    def post(self, request: HttpRequest, chamado_id: int, *args, **kwargs) -> HttpResponse:
        chamado = get_object_or_404(Chamado, pk=chamado_id)
        chamado.gerar_itens_de_instalacao()

        if chamado.status == Chamado.Status.FINALIZADO:
            messages.error(request, "Chamado finalizado. Não é possível alterar.")
            return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

        if chamado.tipo != Chamado.Tipo.ENVIO:
            messages.error(request, "Ação disponível apenas para chamados do tipo ENVIO.")
            return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

        if not chamado.pode_liberar_nf():
            messages.error(
                request,
                "Só é possível informar o contábil após todos os itens estarem OK "
                "(bipados/confirmados).",
            )
            return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

        numero = (request.POST.get("contabilidade_numero") or "").strip()
        if not numero:
            messages.error(request, "Informe o número do chamado contábil.")
            return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

        chamado.contabilidade_numero = numero
        chamado.status = Chamado.Status.AGUARDANDO_NF

        try:
            chamado.full_clean()
        except ValidationError as exc:
            _push_validation_error_messages(request, exc)
            return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

        chamado.save(update_fields=["contabilidade_numero", "status"])
        messages.success(request, "Chamado contábil informado.")
        return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)


class ChamadoInformarNFSaidaView(CapabilityRequiredMixin, View):
    required_capability = "execucao.chamado.editar_referencias"

    @transaction.atomic
    def post(self, request: HttpRequest, chamado_id: int, *args, **kwargs) -> HttpResponse:
        chamado = get_object_or_404(Chamado, pk=chamado_id)

        if chamado.status == Chamado.Status.FINALIZADO:
            messages.error(request, "Chamado finalizado. Não é possível alterar.")
            return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

        if chamado.tipo != Chamado.Tipo.ENVIO:
            messages.error(request, "Ação disponível apenas para chamados do tipo ENVIO.")
            return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

        if not (chamado.contabilidade_numero or "").strip():
            messages.error(request, "Informe o chamado contábil antes da NF de saída.")
            return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

        numero = (request.POST.get("nf_saida_numero") or "").strip()
        if not numero:
            messages.error(request, "Informe o número da NF de saída.")
            return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

        chamado.nf_saida_numero = numero
        chamado.status = Chamado.Status.AGUARDANDO_COLETA

        try:
            chamado.full_clean()
        except ValidationError as exc:
            _push_validation_error_messages(request, exc)
            return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

        chamado.save(update_fields=["nf_saida_numero", "status"])
        messages.success(request, "NF de saída informada.")
        return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)


class ChamadoConfirmarColetaView(CapabilityRequiredMixin, View):
    required_capability = "execucao.chamado.confirmar_coleta"

    @transaction.atomic
    def post(self, request: HttpRequest, chamado_id: int, *args, **kwargs) -> HttpResponse:
        chamado = get_object_or_404(Chamado, pk=chamado_id)

        if chamado.status == Chamado.Status.FINALIZADO:
            messages.error(request, "Chamado finalizado. Não é possível alterar.")
            return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

        if chamado.tipo != Chamado.Tipo.ENVIO:
            messages.error(request, "Ação disponível apenas para chamados do tipo ENVIO.")
            return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

        if not (chamado.nf_saida_numero or "").strip():
            messages.error(request, "Informe a NF de saída antes de confirmar a coleta.")
            return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

        if chamado.coleta_confirmada_em is not None:
            messages.info(request, "Coleta já confirmada.")
            return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

        chamado.coleta_confirmada_em = timezone.now()

        try:
            chamado.full_clean()
        except ValidationError as exc:
            _push_validation_error_messages(request, exc)
            return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

        chamado.save(update_fields=["coleta_confirmada_em"])
        messages.success(request, "Coleta confirmada.")
        return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)


# ==================
# ITENS (SETUP + EXECUÇÃO)
# ==================
class ChamadoAtualizarItensView(CapabilityRequiredMixin, View):
    required_capability = "execucao.chamado.editar_itens"

    @transaction.atomic
    def post(self, request: HttpRequest, chamado_id: int, *args, **kwargs) -> HttpResponse:
        chamado = get_object_or_404(Chamado, pk=chamado_id)

        if chamado.status == Chamado.Status.FINALIZADO:
            messages.warning(request, "Chamado já está finalizado. Não é possível editar itens.")
            return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

        chamado.gerar_itens_de_instalacao()

        itens = list(chamado.itens.select_related("equipamento").all())
        if not itens:
            messages.warning(request, "Este chamado não possui itens para atualizar.")
            return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

        # ==========================
        # MODO SETUP (EM_ABERTURA)
        # ==========================
        if chamado.status == Chamado.Status.EM_ABERTURA:
            for item in itens:
                update_fields: list[str] = []

                deve_configurar = request.POST.get(f"deve_configurar_{item.id}") == "on"
                ip_raw = (request.POST.get(f"ip_{item.id}") or "").strip()

                if not item.equipamento.configuravel:
                    deve_configurar = False
                    ip_raw = ""

                # regra: se deve_configurar=True então IP obrigatório
                if deve_configurar and not ip_raw:
                    messages.error(
                        request,
                        f"Informe o IP do item '{item.equipamento.nome}' (configuração marcada).",
                    )
                    return redirect("execucao:chamado_setup", chamado_id=chamado.id)

                item.deve_configurar = deve_configurar
                item.ip = ip_raw or None
                update_fields += ["deve_configurar", "ip"]
                item.save(update_fields=update_fields)

            # promove para ABERTO (entra na fila)
            chamado.status = Chamado.Status.ABERTO
            chamado.save(update_fields=["status"])

            messages.success(
                request,
                "Setup salvo. Chamado promovido para ABERTO e enviado para a fila.",
            )
            return redirect("execucao:fila")

        # ==========================
        # MODO OPERACIONAL (ABERTO+)
        # ==========================
        for item in itens:
            update_fields: list[str] = []

            deve_configurar = request.POST.get(f"deve_configurar_{item.id}") == "on"
            ip_raw = (request.POST.get(f"ip_{item.id}") or "").strip()

            if not item.equipamento.configuravel:
                deve_configurar = False
                ip_raw = ""

            item.deve_configurar = deve_configurar
            item.ip = ip_raw or None
            update_fields += ["deve_configurar", "ip"]

            if item.tem_ativo:
                item.ativo = (request.POST.get(f"ativo_{item.id}") or "").strip()
                item.numero_serie = (request.POST.get(f"serie_{item.id}") or "").strip()
                update_fields += ["ativo", "numero_serie"]
            else:
                item.confirmado = request.POST.get(f"confirmado_{item.id}") == "on"
                update_fields += ["confirmado"]

            item.save(update_fields=update_fields)

        if chamado.status == Chamado.Status.ABERTO:
            chamado.status = Chamado.Status.EM_EXECUCAO
            chamado.save(update_fields=["status"])

        messages.success(request, "Itens atualizados com sucesso.")
        return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)


class ChamadoFinalizarView(CapabilityRequiredMixin, View):
    required_capability = "execucao.chamado.finalizar"

    @transaction.atomic
    def post(self, request: HttpRequest, chamado_id: int, *args, **kwargs) -> HttpResponse:
        chamado = get_object_or_404(Chamado, pk=chamado_id)
        chamado.gerar_itens_de_instalacao()

        try:
            chamado.finalizar()
        except ValidationError as exc:
            _push_validation_error_messages(request, exc)
            return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

        messages.success(request, "Chamado finalizado com sucesso.")
        return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)


# ==================
# EVIDÊNCIAS
# ==================
class ChamadoAdicionarEvidenciaView(CapabilityRequiredMixin, View):
    required_capability = "execucao.evidencia.upload"

    def post(self, request: HttpRequest, chamado_id: int, *args, **kwargs) -> HttpResponse:
        chamado = get_object_or_404(Chamado, pk=chamado_id)

        tipo = (request.POST.get("tipo") or "").strip()
        descricao = (request.POST.get("descricao") or "").strip()
        arquivo = request.FILES.get("arquivo")

        if not arquivo:
            messages.error(request, "Selecione um arquivo para anexar.")
            return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

        tipos_validos = {t for t, _ in EvidenciaChamado.Tipo.choices}
        if tipo not in tipos_validos:
            messages.error(request, "Tipo de evidência inválido.")
            return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

        EvidenciaChamado.objects.create(
            chamado=chamado,
            tipo=tipo,
            descricao=descricao,
            arquivo=arquivo,
        )

        messages.success(request, "Evidência anexada com sucesso.")
        return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)


class EvidenciaRemoverView(CapabilityRequiredMixin, View):
    required_capability = "execucao.evidencia.remover"

    def post(
        self,
        request: HttpRequest,
        chamado_id: int,
        evidencia_id: int,
        *args,
        **kwargs,
    ) -> HttpResponse:
        chamado = get_object_or_404(Chamado, pk=chamado_id)

        if chamado.finalizado_em:
            messages.error(request, "Chamado finalizado. Não é possível remover evidências.")
            return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

        ev = get_object_or_404(EvidenciaChamado, pk=evidencia_id, chamado_id=chamado.id)
        ev.delete()

        messages.success(request, "Evidência removida.")
        return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)


# ==================
# ITENS / CONFIGURAÇÃO
# ==================
class ItemSetStatusConfiguracaoView(CapabilityRequiredMixin, View):
    required_capability = "execucao.item_configuracao.alterar_status"

    @transaction.atomic
    def post(
        self,
        request: HttpRequest,
        chamado_id: int,
        item_id: int,
        *args,
        **kwargs,
    ) -> HttpResponse:
        chamado = get_object_or_404(Chamado, pk=chamado_id)

        if chamado.finalizado_em:
            messages.error(request, "Chamado finalizado. Não é possível alterar status.")
            return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

        item = get_object_or_404(InstalacaoItem, pk=item_id, chamado=chamado)

        status = (request.POST.get("status") or "").strip()
        motivo = (request.POST.get("motivo") or "").strip()

        validos = {c[0] for c in StatusConfiguracao.choices}
        if status not in validos:
            messages.error(request, "Status inválido.")
            return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

        status_atual = item.status_configuracao

        if (
            status_atual == StatusConfiguracao.CONFIGURADO
            and status != StatusConfiguracao.CONFIGURADO
        ):
            if not motivo:
                messages.error(request, "Informe um motivo para voltar um item já configurado.")
                return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

        if status == status_atual:
            messages.info(request, "Este item já está nesse status.")
            return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

        item.status_configuracao = status
        item.save(update_fields=["status_configuracao"])

        ItemConfiguracaoLog.objects.create(
            item=item,
            de_status=status_atual,
            para_status=status,
            motivo=motivo,
            criado_por=request.user if request.user.is_authenticated else None,
        )

        messages.success(request, "Status de configuração atualizado.")
        return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)
