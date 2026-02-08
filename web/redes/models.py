from django.db import models
from django.db.models import Q


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

    class GatewayPolicy(models.TextChoices):
        OFFSET_FIXO = "OFFSET_FIXO", "Offset fixo (no /24 da loja)"
        DERIVADO_BASE = "DERIVADO_BASE", "Derivado do base_ip"
        FIXO_ABSOLUTO = "FIXO_ABSOLUTO", "IP absoluto"

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

    # MVP de regras de IP
    offset_fixo = models.IntegerField(null=True, blank=True)
    offset_inicio = models.IntegerField(null=True, blank=True)
    offset_fim = models.IntegerField(null=True, blank=True)
    offset_base = models.IntegerField(null=True, blank=True)

    # -----------------------------
    # Evolução (Passo 4): Rede completa por item
    # -----------------------------

    # Máscara (padrão do domínio: CIDR)
    cidr = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="Máscara em CIDR (ex: 24, 27). Preferir CIDR ao invés de máscara pontilhada.",
    )

    # Gateway (com política explícita)
    gateway_policy = models.CharField(
        max_length=20,
        choices=GatewayPolicy.choices,
        null=True,
        blank=True,
        help_text="Como calcular/validar o gateway para este item.",
    )
    gateway_offset = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="Último octeto esperado (ex: 222, 158) quando policy usa offset.",
    )
    gateway_ip = models.GenericIPAddressField(
        protocol="IPv4",
        null=True,
        blank=True,
        help_text="Gateway absoluto quando policy = FIXO_ABSOLUTO.",
    )

    # Hostname
    hostname_pattern = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        help_text="Pattern esperado (ex: NT{cod}X30, LOJA{cod}, TCRH).",
    )
    hostname_examples = models.JSONField(
        null=True,
        blank=True,
        help_text="Opcional: exemplos curtos para documentação/auxílio (não é regra).",
    )

    # reservados (MVP simples) — mantém por compatibilidade
    reservados = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = "Regra de Rede por Equipamento"
        verbose_name_plural = "Regras de Rede por Equipamento"
        ordering = ("perfil_rede__codigo", "codigo")
        constraints = [
            models.UniqueConstraint(
                fields=["perfil_rede", "codigo"],
                name="uniq_regra_rede_equipamento_por_perfil_codigo",
            ),
            # CIDR dentro do range IPv4 (quando preenchido)
            models.CheckConstraint(
                name="ck_cidr_range",
                condition=Q(cidr__isnull=True) | (Q(cidr__gte=1) & Q(cidr__lte=32)),
            ),
            # GatewayPolicy coerente com campos auxiliares
            models.CheckConstraint(
                name="ck_gateway_absoluto_nao_usa_offset",
                condition=(~Q(gateway_policy="FIXO_ABSOLUTO") | Q(gateway_offset__isnull=True)),
            ),
            models.CheckConstraint(
                name="ck_gateway_offset_nao_usa_ip_absoluto",
                condition=(
                    ~Q(gateway_policy__in=["OFFSET_FIXO", "DERIVADO_BASE"])
                    | Q(gateway_ip__isnull=True)
                ),
            ),
            models.CheckConstraint(
                name="ck_gateway_absoluto_requer_gateway_ip",
                condition=(~Q(gateway_policy="FIXO_ABSOLUTO") | Q(gateway_ip__isnull=False)),
            ),
            models.CheckConstraint(
                name="ck_gateway_offset_fixo_requer_gateway_offset",
                condition=(~Q(gateway_policy="OFFSET_FIXO") | Q(gateway_offset__isnull=False)),
            ),
            models.CheckConstraint(
                name="ck_gateway_derivado_requer_gateway_offset",
                condition=(~Q(gateway_policy="DERIVADO_BASE") | Q(gateway_offset__isnull=False)),
            ),
        ]

    def __str__(self) -> str:
        return f"{self.perfil_rede.codigo} :: {self.codigo}"
