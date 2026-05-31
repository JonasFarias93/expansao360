from django.conf import settings
from django.contrib.auth.views import redirect_to_login
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
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path(), settings.LOGIN_URL)
            
        cap = self.required_capability
        if cap:
            if not request.user.is_superuser and not user_has_capability(request.user, cap):
                raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
