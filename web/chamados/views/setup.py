from __future__ import annotations

from django.contrib import messages
from django.db import transaction
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie
from execucao.services.execution_session import usuario_tem_sessao_ativa_no_chamado
from iam.decorators import user_has_capability
from iam.execucao_capabilities import CAP_EXECUCAO_CHAMADO_EDITAR
from iam.mixins import CapabilityRequiredMixin

from ..forms import ChamadoDadosFiscaisForm
from ..models import Chamado, StatusConfiguracao


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


class ChamadoSalvarDadosFiscaisView(View):
    required_capability = "execucao.chamado_editar"

    @transaction.atomic
    def post(
        self, request: HttpRequest, chamado_id: int, *args, **kwargs
    ) -> HttpResponse:
        chamado = get_object_or_404(Chamado, pk=chamado_id)

        if not user_has_capability(request.user, CAP_EXECUCAO_CHAMADO_EDITAR):
            return HttpResponseForbidden("Permissão insuficiente.")

        if not usuario_tem_sessao_ativa_no_chamado(user=request.user, chamado=chamado):
            return HttpResponseForbidden(
                "Sessão ativa é obrigatória para editar este chamado."
            )

        form = ChamadoDadosFiscaisForm(request.POST, instance=chamado)
        if not form.is_valid():
            for errs in form.errors.values():
                for e in errs:
                    messages.error(request, e)
            return redirect("execucao:chamado_setup", chamado_id=chamado.id)

        obj = form.save(commit=False)
        obj.save(update_fields=["contabilidade_numero", "nf_saida_numero"])
        messages.success(request, "Dados salvos com sucesso.")
        return redirect("execucao:chamado_setup", chamado_id=chamado.id)
