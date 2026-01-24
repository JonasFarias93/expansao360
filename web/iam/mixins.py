from __future__ import annotations

from django.contrib import messages
from django.shortcuts import redirect

from iam.decorators import user_has_capability


class CapabilityRequiredMixin:
    """
    Mixin para CBVs com autorização por capability.

    Mantém o mesmo comportamento do decorator:
    - Sem permissão -> messages.error + redirect
    """

    required_capability: str | None = None
    redirect_to: str = "execucao:historico"

    def dispatch(self, request, *args, **kwargs):
        cap = self.required_capability
        if cap and not user_has_capability(request.user, cap):
            messages.error(request, "Você não tem permissão para executar esta ação.")
            return redirect(self.redirect_to)
        return super().dispatch(request, *args, **kwargs)
