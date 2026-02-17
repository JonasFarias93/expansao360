# web/chamados/views/_helpers.py
from __future__ import annotations

from typing import Any

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpRequest


def _is_ajax(request: HttpRequest) -> bool:
    return (
        request.headers.get("X-Requested-With") == "XMLHttpRequest"
        or request.headers.get("x-requested-with") == "XMLHttpRequest"
    )


def _push_validation_error_messages(request: HttpRequest, error: Any) -> None:
    """
    Normaliza mensagens de erro para django.contrib.messages.

    Aceita:
    - ValidationError (com error_dict / error_list / messages)
    - string / qualquer coisa convertível para string (fallback)
    """
    if isinstance(error, ValidationError):
        # error_dict: {field: [msgs]}
        if getattr(error, "error_dict", None):
            for field, errs in error.error_dict.items():
                for e in errs:
                    messages.error(request, f"{field}: {e}")
            return

        # error_list: [errs]
        if getattr(error, "error_list", None):
            for e in error.error_list:
                messages.error(request, str(e))
            return

        # messages: [str]
        if getattr(error, "messages", None):
            for msg in error.messages:
                messages.error(request, str(msg))
            return

        messages.error(request, str(error))
        return

    # dict-like / list-like cases (bem tolerante, sem forçar contrato novo)
    if isinstance(error, dict):
        for k, v in error.items():
            if isinstance(v, (list, tuple, set)):
                for item in v:
                    messages.error(request, f"{k}: {item}")
            else:
                messages.error(request, f"{k}: {v}")
        return

    if isinstance(error, (list, tuple, set)):
        for item in error:
            messages.error(request, str(item))
        return

    messages.error(request, str(error))
