# Create your models here.
from __future__ import annotations
from django.conf import settings
from django.db import models
from django.contrib.auth.models import Group


class Capability(models.Model):
    """
    Capability representa uma permissão atômica (string) para uma ação.
    Ex.: "execucao.chamado.finalizar"
    """

    code = models.CharField(max_length=120, unique=True)
    description = models.CharField(max_length=255, blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["code"]
        verbose_name = "Capability"
        verbose_name_plural = "Capabilities"

    def __str__(self) -> str:  # pragma: no cover
        return self.code


class UserCapability(models.Model):
    """
    Associação explícita entre usuário e capability.
    Mantém rastreabilidade (quem tem o quê) e permite evoluir para grupos/escopos depois.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    capability = models.ForeignKey(Capability, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("user", "capability")]
        indexes = [
            models.Index(fields=["user", "capability"]),
            models.Index(fields=["capability"]),
        ]
        verbose_name = "User Capability"
        verbose_name_plural = "User Capabilities"

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.user} -> {self.capability.code}"


class GroupCapability(models.Model):
    """
    Capabilities associadas a um Group Django.
    Ao adicionar usuário ao grupo, suas capabilities são concedidas automaticamente.
    """
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="capabilities",
    )
    capability = models.ForeignKey(
        Capability,
        on_delete=models.CASCADE,
        related_name="grupos",
    )

    class Meta:
        unique_together = [("group", "capability")]
        verbose_name = "Capability do Grupo"
        verbose_name_plural = "Capabilities dos Grupos"

    def __str__(self) -> str:
        return f"{self.group.name} → {self.capability.code}"