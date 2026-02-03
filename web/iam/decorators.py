from __future__ import annotations

from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect

from .models import UserCapability


def user_has_capability(user, code: str) -> bool:
    if not user or not getattr(user, "is_authenticated", False):
        return False

    # ✅ bypass para superuser
    if getattr(user, "is_superuser", False):
        return True
    return UserCapability.objects.filter(user=user, capability__code=code).exists()


def capability_required(code: str, *, redirect_to="execucao:historico"):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not user_has_capability(request.user, code):
                messages.error(request, "Você não tem permissão para executar esta ação.")
                return redirect(redirect_to)
            return view_func(request, *args, **kwargs)

        return _wrapped

    return decorator
