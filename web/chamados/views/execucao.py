from __future__ import annotations

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View
from django.views.generic import TemplateView
from iam.decorators import user_has_capability
from iam.execucao_capabilities import (
    CAP_EXECUCAO_CHAMADO_EDITAR,
    CAP_EXECUCAO_CHAMADO_FINALIZAR,
)
from iam.mixins import CapabilityRequiredMixin

from chamados.services.chamado_status import recalcular_status
from chamados.services.finalizacao import validar_finalizacao
from execucao.services.execution_session import (
    end_session_exit,
    usuario_tem_sessao_ativa_no_chamado,
)

from ..forms import ChamadoDadosFiscaisForm
from ..models import Chamado, EvidenciaChamado, StatusConfiguracao


class ChamadoExecucaoView(CapabilityRequiredMixin, TemplateView):
    template_name = "execucao/chamado_execucao.html"
    required_capability = "execucao.chamado.visualizar"

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        chamado_id = kwargs["chamado_id"]
        chamado = get_object_or_404(Chamado, pk=chamado_id)

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

        sessao_ativa = usuario_tem_sessao_ativa_no_chamado(
            user=self.request.user,
            chamado=chamado,
        )

        is_envio = chamado.tipo == Chamado.Tipo.ENVIO
        is_retorno = chamado.tipo == Chamado.Tipo.RETORNO

        gate_contabil_ok = bool((chamado.contabilidade_numero or "").strip())
        gate_nf_ok = bool((chamado.nf_saida_numero or "").strip())
        gate_coleta_ok = chamado.coleta_confirmada_em is not None

        can_edit_dados_fiscais = (
            user_has_capability(self.request.user, CAP_EXECUCAO_CHAMADO_EDITAR)
            and sessao_ativa
        )

        can_confirmar_coleta = (
            user_has_capability(self.request.user, CAP_EXECUCAO_CHAMADO_EDITAR)
            and sessao_ativa
        )

        can_finalizar = (
            user_has_capability(self.request.user, CAP_EXECUCAO_CHAMADO_FINALIZAR)
            and sessao_ativa
        )

        can_execute_actions = bool(can_confirmar_coleta or can_finalizar)

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

        # Mantém o gate de confirmar coleta como regra de UI (fluxo de ENVIO)
        pode_confirmar_coleta = (
            can_confirmar_coleta
            and is_envio
            and chamado.status != Chamado.Status.FINALIZADO
            and not gate_coleta_ok
            and gate_nf_ok
        )

        # ✅ Fonte única para "pode finalizar": mesma regra do endpoint AJAX (service)
        validacao_finalizacao = validar_finalizacao(chamado)

        # IMPORTANTE:
        # - Não duplicar regras fiscais/config/coleta aqui, para não divergir do service.
        # - A UI habilita "Finalizar" quando o service diz que não há pendências.
        pode_finalizar = (
            can_finalizar
            and chamado.status != Chamado.Status.FINALIZADO
            and validacao_finalizacao.ok
        )

        has_session = bool(sessao_ativa)
        can_edit = bool(sessao_ativa and chamado.status != Chamado.Status.FINALIZADO)
        can_finalize = bool(pode_finalizar)

        evidencias = EvidenciaChamado.objects.filter(chamado=chamado).order_by(
            "-criado_em",
            "-id",
        )
        evidencia_tipos = list(EvidenciaChamado.Tipo.choices)

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
                "can_edit_dados_fiscais": can_edit_dados_fiscais,
                "dados_fiscais_form": ChamadoDadosFiscaisForm(instance=chamado),
                "can_execute_actions": can_execute_actions,
                "pode_confirmar_coleta": pode_confirmar_coleta,
                "pode_finalizar": pode_finalizar,
                "has_session": has_session,
                "can_edit": can_edit,
                "can_finalize": can_finalize,
                # útil para UI/debug futuro (opcional, mas seguro)
                "validacao_finalizacao": validacao_finalizacao,
            }
        )
        return ctx


class ChamadoSalvarExecucaoView(CapabilityRequiredMixin, View):
    required_capability = "execucao.chamado_editar"

    @transaction.atomic
    def post(
        self, request: HttpRequest, chamado_id: int, *args, **kwargs
    ) -> HttpResponse:
        chamado = get_object_or_404(Chamado, pk=chamado_id)

        is_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest"

        if not usuario_tem_sessao_ativa_no_chamado(user=request.user, chamado=chamado):
            raise PermissionDenied

        itens = list(chamado.itens.all())
        for item in itens:
            changed_fields: list[str] = []

            key_ativo = f"ativo_{item.id}"
            key_serie = f"serie_{item.id}"
            key_conf = f"confirmado_{item.id}"

            if key_ativo in request.POST:
                item.ativo = (request.POST.get(key_ativo) or "").strip()
                changed_fields.append("ativo")

            if key_serie in request.POST:
                item.numero_serie = (request.POST.get(key_serie) or "").strip()
                changed_fields.append("numero_serie")

            if key_conf in request.POST:
                item.confirmado = True
                changed_fields.append("confirmado")

            if changed_fields:
                item.save(update_fields=changed_fields)

        form = ChamadoDadosFiscaisForm(request.POST, instance=chamado)
        if form.is_valid():
            form.save()
        else:
            if is_ajax:
                return JsonResponse(
                    {"ok": False, "error": "dados_fiscais_invalidos"},
                    status=400,
                )
            messages.error(request, "Dados fiscais inválidos. Verifique os campos.")
            return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

        novo_status = recalcular_status(chamado)
        if novo_status != chamado.status:
            chamado.status = novo_status
            chamado.save(update_fields=["status"])

        hora = timezone.localtime().strftime("%H:%M")
        msg = f"Salvo por {request.user} às {hora}"
        messages.success(request, msg)

        if is_ajax:
            return JsonResponse(
                {
                    "ok": True,
                    "saved_at": hora,
                    "message": msg,
                }
            )

        return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)


class ChamadoEncerrarSessaoView(CapabilityRequiredMixin, View):
    required_capability = "execucao.chamado_editar"

    @transaction.atomic
    def post(
        self, request: HttpRequest, chamado_id: int, *args, **kwargs
    ) -> HttpResponse:
        chamado = get_object_or_404(Chamado, pk=chamado_id)
        is_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest"

        ended = end_session_exit(chamado=chamado, actor=request.user)

        if is_ajax:
            return JsonResponse({"ok": True, "ended": bool(ended)})

        if ended:
            messages.success(request, "Sessão encerrada.")
        else:
            messages.info(request, "Nenhuma sessão ativa para encerrar.")

        next_url = request.GET.get("next")
        if next_url and url_has_allowed_host_and_scheme(
            next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            return redirect(next_url)

        return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)
