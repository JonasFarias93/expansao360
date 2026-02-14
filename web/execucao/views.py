# web/execucao/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from iam.decorators import user_has_capability
from iam.execucao_capabilities import CAP_EXECUCAO_CHAMADO_EDITAR

from execucao.services.execution_session import (
    NoActiveSessionToTakeError,
    take_session,
)
from execucao.services.open_session import SessionBlockedError, open_session

from .models import (
    Chamado,
)


@login_required
@require_POST
def chamado_abrir(request, chamado_id: int):
    if not user_has_capability(request.user, CAP_EXECUCAO_CHAMADO_EDITAR):
        raise PermissionDenied

    chamado = get_object_or_404(Chamado, pk=chamado_id)

    try:
        open_session(chamado=chamado, user=request.user)
    except SessionBlockedError:
        from execucao.services.execution_session import get_active_session

        active = get_active_session(chamado=chamado)
        if active is not None:
            messages.error(
                request,
                (
                    f"Chamado em execução por {active.usuario} "
                    f"desde {active.started_at:%d/%m/%Y %H:%M}."
                ),
            )
        else:
            messages.error(request, "Chamado em execução por outro usuário.")

        return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)

    # Direciona para a tela “editável” correta
    if chamado.status == Chamado.Status.ABERTO:
        return redirect("execucao:chamado_setup", chamado_id=chamado.id)

    return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)


@login_required
@require_POST
def chamado_take_session(request, chamado_id: int):
    chamado = get_object_or_404(Chamado, pk=chamado_id)

    # Permissão é enforced no serviço (IAM como autoridade).
    # Se preferir “perm primeiro” como no abrir, dá pra checar aqui também,
    # mas manter no serviço evita duplicação.
    try:
        take_session(chamado=chamado, actor=request.user)
    except NoActiveSessionToTakeError:
        return HttpResponseBadRequest("Não há sessão ativa para tomar.")

    messages.success(
        request,
        "Sessão tomada com sucesso. Você está editando este chamado.",
    )

    # Direciona para a tela “editável” correta (mesmo fluxo do abrir)
    if chamado.status == Chamado.Status.ABERTO:
        return redirect("execucao:chamado_setup", chamado_id=chamado.id)

    return redirect("execucao:chamado_detalhe", chamado_id=chamado.id)
