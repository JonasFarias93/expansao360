# web/users/backends.py
from __future__ import annotations

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpRequest


class OperationalAuthBackend(ModelBackend):
    """
    Backend de autenticação que respeita o status operacional do UserProfile.
    Bloqueia login de usuários AFASTADO, BLOQUEADO ou DESLIGADO.
    """

    def authenticate(
        self,
        request: HttpRequest | None,
        username: str | None = None,
        password: str | None = None,
        **kwargs,
    ) -> AbstractBaseUser | None:
        user = super().authenticate(request, username=username, password=password, **kwargs)
        if user is None:
            return None

        profile = getattr(user, "profile", None)
        if profile is not None and not profile.is_operacional:
            return None

        return user