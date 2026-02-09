from __future__ import annotations

from django.core.exceptions import PermissionDenied

from iam.decorators import user_has_capability


class CapabilityRequiredMixin:
    """
    Mixin para CBVs com autorização por capability.

    - Sem permissão -> PermissionDenied
    - Preserva ciclo de middlewares (CSRF, messages, etc.)
    """

    required_capability: str | None = None

    def dispatch(self, request, *args, **kwargs):
        cap = self.required_capability
        if cap and not user_has_capability(request.user, cap):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
