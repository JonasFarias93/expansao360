from __future__ import annotations

from django.db.models import Q
from django.views.generic import TemplateView
from iam.mixins import CapabilityRequiredMixin

from ..models import Chamado


class HistoricoView(CapabilityRequiredMixin, TemplateView):
    template_name = "execucao/historico_chamados.html"
    required_capability = "execucao.chamado.visualizar"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        q = (self.request.GET.get("q") or "").strip()
        java = (self.request.GET.get("java") or "").strip()

        chamados = (
            Chamado.objects.all()
            .select_related("loja", "projeto")
            .order_by("-criado_em")
        )

        if java:
            chamados = chamados.filter(loja__codigo__startswith=java)

        if q:
            chamados = chamados.filter(
                Q(protocolo__icontains=q)
                | Q(ticket_externo_id__icontains=q)
                | Q(ticket_externo_sistema__icontains=q)
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
        ctx["java"] = java
        ctx["chamados"] = chamados[:200]
        return ctx
