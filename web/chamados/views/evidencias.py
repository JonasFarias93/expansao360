from __future__ import annotations

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from iam.mixins import CapabilityRequiredMixin

from ..models import Chamado, EvidenciaChamado


class ChamadoAdicionarEvidenciaView(CapabilityRequiredMixin, View):
    required_capability = "execucao.evidencia.upload"

    def get(
        self, request: HttpRequest, chamado_id: int, *args, **kwargs
    ) -> HttpResponse:
        get_object_or_404(Chamado, pk=chamado_id)
        return redirect("chamados:chamado_detalhe", chamado_id=chamado_id)

    def post(
        self, request: HttpRequest, chamado_id: int, *args, **kwargs
    ) -> HttpResponse:
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
            messages.error(
                request, "Chamado finalizado. Não é possível remover evidências."
            )
            return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

        ev = get_object_or_404(EvidenciaChamado, pk=evidencia_id, chamado_id=chamado.id)
        ev.delete()

        messages.success(request, "Evidência removida.")
        return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)
