from __future__ import annotations

from django.contrib import messages
from django.db import transaction
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views import View
from execucao.services.execution_session import usuario_tem_sessao_ativa_no_chamado
from iam.mixins import CapabilityRequiredMixin

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

        if chamado.status == Chamado.Status.FINALIZADO:
            messages.warning(
                request, "Chamado já está finalizado. Não é possível editar itens."
            )
            return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

        chamado.gerar_itens_de_instalacao()

        itens = list(chamado.itens.select_related("equipamento").all())
        if not itens:
            messages.warning(request, "Este chamado não possui itens para atualizar.")
            return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

        if chamado.status == Chamado.Status.EM_ABERTURA:
            for item in itens:
                update_fields: list[str] = []

                deve_configurar = request.POST.get(f"deve_configurar_{item.id}") == "on"
                ip_raw = (request.POST.get(f"ip_{item.id}") or "").strip()

                if not item.equipamento.configuravel:
                    deve_configurar = False
                    ip_raw = ""

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

            chamado.status = Chamado.Status.ABERTO
            chamado.save(update_fields=["status"])

            messages.success(
                request,
                "Setup salvo. Chamado promovido para ABERTO e enviado para a fila.",
            )
            return redirect("execucao:fila")

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
