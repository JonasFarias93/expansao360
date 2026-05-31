# web/historico/views.py
from __future__ import annotations

from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from iam.mixins import CapabilityRequiredMixin
from historico.models import HistoricoExecucao, HistoricoAtivoTimeline


class HistoricoExecucaoDetalheView(CapabilityRequiredMixin, TemplateView):
    template_name = "historico/detalhe_execucao.html"
    required_capability = "execucao.chamado.visualizar"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        historico = get_object_or_404(
            HistoricoExecucao, chamado_id=kwargs["chamado_id"]
        )
        ctx["historico"] = historico
        return ctx


class HistoricoLojaView(CapabilityRequiredMixin, TemplateView):
    template_name = "historico/loja.html"
    required_capability = "execucao.chamado.visualizar"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        loja_codigo = kwargs["loja_codigo"]
        historicos = HistoricoExecucao.objects.filter(
            loja_codigo=loja_codigo
        ).order_by("-finalizado_em", "-criado_em")
        ctx["loja_codigo"] = loja_codigo
        ctx["loja_nome"] = historicos.first().loja_nome if historicos.exists() else ""
        ctx["historicos"] = historicos
        return ctx


class HistoricoAtivoTimelineView(CapabilityRequiredMixin, TemplateView):
    template_name = "historico/ativo_timeline.html"
    required_capability = "execucao.chamado.visualizar"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ativo = kwargs["ativo"]
        timeline = HistoricoAtivoTimeline.objects.filter(
            ativo=ativo
        ).order_by("-ocorrido_em")
        ctx["ativo"] = ativo
        ctx["timeline"] = timeline
        return ctx