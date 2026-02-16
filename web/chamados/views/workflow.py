from __future__ import annotations

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views import View
from execucao.services.execution_session import get_active_session
from iam.execucao_capabilities import CAP_EXECUCAO_CHAMADO_FINALIZAR
from iam.mixins import CapabilityRequiredMixin

from chamados.services.finalizacao import validar_finalizacao

from ..models import Chamado


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


class ChamadoInformarContabilView(CapabilityRequiredMixin, View):
    required_capability = "execucao.chamado.editar_referencias"

    @transaction.atomic
    def post(
        self, request: HttpRequest, chamado_id: int, *args, **kwargs
    ) -> HttpResponse:
        chamado = get_object_or_404(Chamado, pk=chamado_id)
        chamado.gerar_itens_de_instalacao()

        if chamado.status == Chamado.Status.FINALIZADO:
            messages.error(request, "Chamado finalizado. Não é possível alterar.")
            return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

        if chamado.tipo != Chamado.Tipo.ENVIO:
            messages.error(
                request, "Ação disponível apenas para chamados do tipo ENVIO."
            )
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
    def post(
        self, request: HttpRequest, chamado_id: int, *args, **kwargs
    ) -> HttpResponse:
        chamado = get_object_or_404(Chamado, pk=chamado_id)

        if chamado.status == Chamado.Status.FINALIZADO:
            messages.error(request, "Chamado finalizado. Não é possível alterar.")
            return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

        if chamado.tipo != Chamado.Tipo.ENVIO:
            messages.error(
                request, "Ação disponível apenas para chamados do tipo ENVIO."
            )
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
    def post(
        self, request: HttpRequest, chamado_id: int, *args, **kwargs
    ) -> HttpResponse:
        chamado = (
            Chamado.objects.select_for_update()
            .select_related("loja", "projeto", "subprojeto", "kit")
            .get(pk=chamado_id)
        )

        if chamado.status == Chamado.Status.FINALIZADO:
            messages.error(request, "Chamado finalizado. Não é possível alterar.")
            return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

        if chamado.tipo != Chamado.Tipo.ENVIO:
            messages.error(
                request, "Ação disponível apenas para chamados do tipo ENVIO."
            )
            return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

        if not (chamado.nf_saida_numero or "").strip():
            messages.error(
                request, "Informe a NF de saída antes de confirmar a coleta."
            )
            return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

        if chamado.coleta_confirmada_em is not None:
            messages.info(request, "Coleta já confirmada.")
            return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

        chamado.coleta_confirmada = True
        chamado.coleta_confirmada_em = timezone.now()
        chamado.coleta_confirmada_por = (
            request.user if request.user.is_authenticated else None
        )

        try:
            chamado.full_clean()
        except ValidationError as exc:
            _push_validation_error_messages(request, exc)
            return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

        chamado.save(
            update_fields=[
                "coleta_confirmada",
                "coleta_confirmada_em",
                "coleta_confirmada_por",
            ]
        )
        messages.success(request, "Coleta confirmada.")
        return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)


class ChamadoFinalizarView(CapabilityRequiredMixin, View):
    required_capability = CAP_EXECUCAO_CHAMADO_FINALIZAR

    @transaction.atomic
    def post(
        self, request: HttpRequest, chamado_id: int, *args, **kwargs
    ) -> HttpResponse:
        chamado = get_object_or_404(
            Chamado.objects.select_for_update().select_related(
                "loja", "projeto", "subprojeto", "kit"
            ),
            pk=chamado_id,
        )

        if chamado.status == Chamado.Status.FINALIZADO:
            messages.info(request, "Chamado já está finalizado.")
            return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

        sessao = get_active_session(chamado=chamado)
        if sessao is None:
            if _is_ajax(request):
                return JsonResponse({"ok": False, "error": "SEM_SESSAO"}, status=403)
            return HttpResponseForbidden("Sem sessão ativa no chamado.")

        result = validar_finalizacao(chamado)

        if not result.ok:
            if _is_ajax(request):
                return JsonResponse(
                    {
                        "ok": False,
                        "pendencias": {
                            "fiscais": [p.__dict__ for p in result.fiscais],
                            "coleta": [p.__dict__ for p in result.coleta],
                            "itens": [p.__dict__ for p in result.itens],
                        },
                    },
                    status=400,
                )

            messages.error(request, "Não é possível finalizar. Existem pendências:")
            for p in result.fiscais:
                messages.error(request, f"Fiscal: {p.message}")
            for p in result.coleta:
                messages.error(request, f"Coleta: {p.message}")
            for it in result.itens[:20]:
                messages.error(
                    request, f"Item {it.item_id} ({it.equipamento}): {it.message}"
                )
            if len(result.itens) > 20:
                messages.error(
                    request,
                    f"... e mais {len(result.itens) - 20} pendência(s) de itens.",
                )

            return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

        chamado.status = Chamado.Status.FINALIZADO

        sessao.ended_at = timezone.now()
        sessao.ended_reason = "FINALIZE"
        sessao.save(update_fields=["ended_at", "ended_reason"])

        chamado.save(update_fields=["status"])

        _registrar_log_finalizacao(chamado=chamado, user=request.user)

        hhmm = timezone.localtime().strftime("%H:%M")
        messages.success(request, f"Finalizado por {request.user} às {hhmm}.")

        if _is_ajax(request):
            return JsonResponse({"ok": True, "status": chamado.status}, status=200)

        return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)


def _is_ajax(request: HttpRequest) -> bool:
    return request.headers.get("X-Requested-With") == "XMLHttpRequest"


def _registrar_log_finalizacao(*, chamado: Chamado, user) -> None:
    fn = getattr(chamado, "registrar_log", None)
    if callable(fn):
        fn(f"Finalizado por {user}.")
        return
    return
