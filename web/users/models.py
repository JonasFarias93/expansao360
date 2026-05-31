# web/users/models.py
from __future__ import annotations

from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    """
    Contexto operacional do usuário.
    Extensão de auth.User — nunca substitui, apenas complementa.
    """

    class Status(models.TextChoices):
        ATIVO = "ATIVO", "Ativo"
        AFASTADO = "AFASTADO", "Afastado"
        BLOQUEADO = "BLOQUEADO", "Bloqueado"
        DESLIGADO = "DESLIGADO", "Desligado"

    class Perfil(models.TextChoices):
        TECNICO = "TECNICO", "Técnico de Campo"
        COORDENADOR = "COORDENADOR", "Coordenador"
        LOGISTICA = "LOGISTICA", "Logística"
        AUDITOR = "AUDITOR", "Auditor"
        ADMINISTRADOR = "ADMINISTRADOR", "Administrador"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="profile",
    )

    perfil = models.CharField(
        max_length=20,
        choices=Perfil.choices,
        default=Perfil.TECNICO,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ATIVO,
    )

    equipe = models.CharField(max_length=80, blank=True, default="")
    supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="supervisionados",
    )

    observacoes = models.TextField(blank=True, default="")

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Perfil de Usuário"
        verbose_name_plural = "Perfis de Usuários"

    def __str__(self) -> str:
        return f"{self.user.username} ({self.get_perfil_display()})"

    @property
    def is_operacional(self) -> bool:
        """Usuário pode operar no sistema."""
        return self.status == self.Status.ATIVO