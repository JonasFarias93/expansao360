# web/execucao/models.py


from __future__ import annotations

from datetime import timedelta

# =========
# imports
# =========
from chamados.models import (  # noqa: F401,E402
    NF_SAIDA_ONLY_DIGITS_ERROR,
    Chamado,
    EvidenciaChamado,
    InstalacaoItem,
    ItemConfiguracaoLog,
    StatusConfiguracao,
)
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone

# =====================================
# ExecutionSession
# ====================================


def _default_expires_at():
    # dado: agora + 2h (sem job ainda; só dado)
    return timezone.now() + timedelta(hours=2)


class ExecutionSessionQuerySet(models.QuerySet):
    def active(self) -> ExecutionSessionQuerySet:
        return self.filter(ended_at__isnull=True, expires_at__gt=timezone.now())


class ExecutionSession(models.Model):
    class EndReason(models.TextChoices):
        FINALIZADO = "FINALIZADO", "Finalizado"
        CANCELADO = "CANCELADO", "Cancelado"
        TIMEOUT = "TIMEOUT", "Timeout"
        OUTRO = "OUTRO", "Outro"
        ADMIN_TAKE = "ADMIN_TAKE", "Admin tomou a sessão"
        SAVE = "SAVE", "Salvar execução"
        USER_EXIT = "USER_EXIT", "Usuário saiu da execução"

    chamado = models.ForeignKey(
        Chamado,
        on_delete=models.CASCADE,
        related_name="execution_sessions",
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="execution_sessions",
    )

    started_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(default=_default_expires_at)

    ended_at = models.DateTimeField(null=True, blank=True)
    ended_reason = models.CharField(
        max_length=20,
        choices=EndReason.choices,
        null=True,
        blank=True,
    )

    objects = ExecutionSessionQuerySet.as_manager()

    class Meta:
        constraints = [
            # “sessão ativa” == ended_at is null AND expires_at > now()
            models.UniqueConstraint(
                fields=["chamado"],
                condition=Q(ended_at__isnull=True),
                name="uniq_open_execution_session_per_chamado",
            )
        ]
        indexes = [
            models.Index(fields=["chamado", "ended_at"]),
            models.Index(fields=["usuario", "ended_at"]),
            models.Index(fields=["expires_at"]),
        ]

    def __str__(self) -> str:
        return f"ExecutionSession(chamado_id={self.chamado_id}, usuario_id={self.usuario_id})"

    @property
    def is_active(self) -> bool:
        return self.ended_at is None and self.expires_at > timezone.now()

    def end(self, reason: str | None = None) -> None:
        if self.ended_at is None:
            self.ended_at = timezone.now()
            if reason:
                self.ended_reason = reason


class ExecutionSessionLog(models.Model):
    class Reason(models.TextChoices):
        ADMIN_TAKE = "ADMIN_TAKE", "Admin tomou a sessão"

    chamado = models.ForeignKey(
        Chamado,
        on_delete=models.CASCADE,
        related_name="session_logs",
    )
    previous_usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    new_usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="+",
    )
    reason = models.CharField(
        max_length=32,
        choices=Reason.choices,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
