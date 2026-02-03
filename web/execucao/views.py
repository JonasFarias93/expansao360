# web/execucao/views.py
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Case, IntegerField, Q, Value, When
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
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

# ==================
# HISTÓRICO
# ==================


class ChamadoCreateView(CapabilityRequiredMixin, View):
    required_capability = "execucao.chamado.criar"
    template_name = "execucao/chamado_create.html"

    def get(self, request):
        form = ChamadoCreateForm()
        return render(request, self.template_name, {"form": form})

    @transaction.atomic
    def post(self, request):
        form = ChamadoCreateForm(request.POST)

        if not form.is_valid():
            return render(request, self.template_name, {"form": form})

        chamado = Chamado.objects.create(
            loja=form.cleaned_data["loja"],
            projeto=form.cleaned_data["projeto"],
            subprojeto=form.cleaned_data["subprojeto"],
            kit=form.cleaned_data["kit"],
            status=Chamado.Status.ABERTO,
            tipo=Chamado.Tipo.ENVIO,
        )

        chamado.gerar_itens_de_instalacao()

        messages.success(
            request,
            f"Chamado {chamado.protocolo} aberto com sucesso.",
        )
        return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)


class ChamadoFilaView(CapabilityRequiredMixin, TemplateView):
    """
    Fila operacional de chamados ativos (ABERTO / EM_EXECUCAO).
    """

    template_name = "execucao/fila.html"
    required_capability = "execucao.chamado.visualizar"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        chamados = (
            Chamado.objects.filter(status__in=[Chamado.Status.ABERTO, Chamado.Status.EM_EXECUCAO])
            .select_related("loja", "projeto")
            .annotate(
                prioridade=Case(
                    When(status=Chamado.Status.EM_EXECUCAO, then=Value(0)),
                    When(status=Chamado.Status.ABERTO, then=Value(1)),
                    default=Value(2),
                    output_field=IntegerField(),
                )
            )
            .order_by("prioridade", "criado_em")
        )

        ctx["chamados"] = chamados
        return ctx


class HistoricoView(CapabilityRequiredMixin, TemplateView):
    template_name = "execucao/historico.html"
    required_capability = "execucao.chamado.visualizar"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        q = (self.request.GET.get("q") or "").strip()

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

        ctx["q"] = q
        ctx["chamados"] = chamados[:200]  # limite simples para não pesar

        return ctx


# ==================
# CHAMADO
# ==================
class ChamadoDetailView(CapabilityRequiredMixin, TemplateView):
    template_name = "execucao/chamado_detalhe.html"
    required_capability = "execucao.chamado.visualizar"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        chamado_id = kwargs["chamado_id"]

        chamado = get_object_or_404(
            Chamado.objects.select_related("loja", "projeto", "subprojeto", "kit"),
            pk=chamado_id,
        )

        # Mantém exatamente como estava na FBV
        chamado.gerar_itens_de_instalacao()

        itens_qs = chamado.itens.select_related("equipamento").all().order_by("id")

        config_total = itens_qs.filter(requer_configuracao=True).count()
        config_done = itens_qs.filter(
            requer_configuracao=True,
            status_configuracao=StatusConfiguracao.CONFIGURADO,
        ).count()
        config_pct = int((config_done * 100) / config_total) if config_total else 0

        itens = list(itens_qs)

        evidencias = EvidenciaChamado.objects.filter(chamado=chamado).order_by("-criado_em", "-id")
        evidencia_tipos = list(EvidenciaChamado.Tipo.choices)

        ctx.update(
            {
                "chamado": chamado,
                "itens": itens,
                "evidencias": evidencias,
                "evidencia_tipos": evidencia_tipos,
                "config_total": config_total,
                "config_done": config_done,
                "config_pct": config_pct,
            }
        )
        return ctx


class ChamadoAtualizarItensView(CapabilityRequiredMixin, View):
    required_capability = "execucao.chamado.editar_itens"

    @transaction.atomic
    def post(self, request, chamado_id, *args, **kwargs):
        chamado = get_object_or_404(Chamado, pk=chamado_id)

        if chamado.status == Chamado.Status.FINALIZADO:
            messages.warning(
                request,
                "Chamado já está finalizado. Não é possível editar itens.",
            )
            return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

        chamado.gerar_itens_de_instalacao()

        itens = list(chamado.itens.select_related("equipamento").all())
        if not itens:
            messages.warning(request, "Este chamado não possui itens para atualizar.")
            return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

        for item in itens:
            if item.tem_ativo:
                item.ativo = (request.POST.get(f"ativo_{item.id}") or "").strip()
                item.numero_serie = (request.POST.get(f"serie_{item.id}") or "").strip()
                item.save(update_fields=["ativo", "numero_serie"])
            else:
                item.confirmado = request.POST.get(f"confirmado_{item.id}") == "on"
                item.save(update_fields=["confirmado"])

        if chamado.status == Chamado.Status.ABERTO:
            chamado.status = Chamado.Status.EM_EXECUCAO
            chamado.save(update_fields=["status"])

        messages.success(request, "Itens atualizados com sucesso.")
        return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)


class ChamadoFinalizarView(CapabilityRequiredMixin, View):
    required_capability = "execucao.chamado.finalizar"

    def post(self, request, chamado_id, *args, **kwargs):
        chamado = get_object_or_404(Chamado, pk=chamado_id)
        chamado.gerar_itens_de_instalacao()

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


# ==================
# EVIDÊNCIAS
# ==================
class ChamadoAdicionarEvidenciaView(CapabilityRequiredMixin, View):
    required_capability = "execucao.evidencia.upload"

    def post(self, request, chamado_id, *args, **kwargs):
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

    def post(self, request, chamado_id, evidencia_id, *args, **kwargs):
        chamado = get_object_or_404(Chamado, pk=chamado_id)

        if chamado.finalizado_em:
            messages.error(request, "Chamado finalizado. Não é possível remover evidências.")
            return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

        ev = get_object_or_404(EvidenciaChamado, pk=evidencia_id, chamado_id=chamado.id)
        ev.delete()

        messages.success(request, "Evidência removida com sucesso.")
        return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)


# ==================
# ITENS / CONFIGURAÇÃO
# ==================


class ItemSetStatusConfiguracaoView(CapabilityRequiredMixin, View):
    required_capability = "execucao.item_configuracao.alterar_status"

    def post(self, request, chamado_id, item_id, *args, **kwargs):
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
