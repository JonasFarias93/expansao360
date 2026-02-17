from __future__ import annotations

from django.contrib import messages
from django.db import transaction
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views import View
from execucao.services.execution_session import usuario_tem_sessao_ativa_no_chamado
from iam.mixins import CapabilityRequiredMixin
from chamados.services.itens_update import atualizar_itens

from ..models import (
    Chamado,
    InstalacaoItem,
    ItemConfiguracaoLog,
    StatusConfiguracao,
)


class ChamadoAtualizarItensView(CapabilityRequiredMixin, View):
    required_capability = "execucao.chamado.editar_itens"

    @transaction.atomic
    def post(
        self, request: HttpRequest, chamado_id: int, *args, **kwargs
    ) -> HttpResponse:
        chamado = get_object_or_404(Chamado, pk=chamado_id)

        result = atualizar_itens(chamado=chamado, post_data=request.POST)

        for m in result.messages:
            getattr(messages, m.level)(request, m.text)

        return redirect(result.redirect_name, **result.redirect_kwargs)


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
            messages.error(
                request, "Chamado finalizado. Não é possível alterar status."
            )
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
                messages.error(
                    request, "Informe um motivo para voltar um item já configurado."
                )
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


class ItemMarcarConfiguradoView(CapabilityRequiredMixin, View):
    required_capability = "execucao.chamado_editar"

    @transaction.atomic
    def post(self, request: HttpRequest, item_id: int, *args, **kwargs) -> HttpResponse:
        item = get_object_or_404(
            InstalacaoItem.objects.select_related("chamado", "configurado_por"),
            pk=item_id,
        )
        chamado = item.chamado

        if not usuario_tem_sessao_ativa_no_chamado(user=request.user, chamado=chamado):
            return JsonResponse({"ok": False, "error": "SESSAO_INATIVA"}, status=403)

        if item.configurado_em is not None:
            return JsonResponse(
                {
                    "ok": True,
                    "already_configured": True,
                    "item_id": item.id,
                    "configurado_em": item.configurado_em.isoformat(),
                    "configurado_por": getattr(item.configurado_por, "username", None),
                },
                status=200,
            )

        item.configurado_em = timezone.now()
        item.configurado_por = request.user
        item.save(update_fields=["configurado_em", "configurado_por"])

        return JsonResponse(
            {
                "ok": True,
                "already_configured": False,
                "item_id": item.id,
                "configurado_em": item.configurado_em.isoformat(),
                "configurado_por": getattr(item.configurado_por, "username", None),
            },
            status=200,
        )
