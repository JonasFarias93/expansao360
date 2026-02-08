from django.db import models


class PerfilRede(models.Model):
    class Tipo(models.TextChoices):
        LEGACY_FLAT = "LEGACY_FLAT", "Legacy Flat"
        SEGMENTADO = "SEGMENTADO", "Segmentado"

    codigo = models.SlugField(max_length=64, unique=True)
    descricao = models.CharField(max_length=255)
    ativo = models.BooleanField(default=True)
    tipo = models.CharField(max_length=20, choices=Tipo.choices)

    class Meta:
        verbose_name = "Perfil de Rede"
        verbose_name_plural = "Perfis de Rede"
        ordering = ("codigo",)

    def __str__(self) -> str:
        return self.codigo


class RegraRedeEquipamento(models.Model):
    class IpPolicy(models.TextChoices):
        OFFSET_FIXO = "OFFSET_FIXO", "Offset fixo"
        SEQUENCIAL = "SEQUENCIAL", "Sequencial"
        FAIXA = "FAIXA", "Faixa"

    codigo = models.SlugField(
        max_length=64,
        help_text="Tipo do equipamento (ex: PDV, TC, CONSULTA_PRECO).",
    )
    descricao = models.CharField(max_length=255)

    perfil_rede = models.ForeignKey(
        PerfilRede,
        on_delete=models.PROTECT,
        related_name="regras_equipamento",
    )

    ip_policy = models.CharField(max_length=20, choices=IpPolicy.choices)

    # MVP de regras
    offset_fixo = models.IntegerField(null=True, blank=True)

    offset_inicio = models.IntegerField(null=True, blank=True)
    offset_fim = models.IntegerField(null=True, blank=True)

    offset_base = models.IntegerField(null=True, blank=True)

    # reservados (MVP simples)
    reservados = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = "Regra de Rede por Equipamento"
        verbose_name_plural = "Regras de Rede por Equipamento"
        ordering = ("perfil_rede__codigo", "codigo")
        constraints = [
            models.UniqueConstraint(
                fields=["perfil_rede", "codigo"],
                name="uniq_regra_rede_equipamento_por_perfil_codigo",
            )
        ]

    def __str__(self) -> str:
        return f"{self.perfil_rede.codigo} :: {self.codigo}"
