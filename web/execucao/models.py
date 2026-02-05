# web/execucao/models.py

from __future__ import annotations

# =========
# imports
# =========
import secrets

from cadastro.models import Equipamento, Kit, Loja, Projeto, Subprojeto
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import IntegrityError, models, transaction
from django.utils import timezone


# ==================
# status configuração
# ==================
class StatusConfiguracao(models.TextChoices):
    AGUARDANDO = "AGUARDANDO", "Aguardando"
    EM_CONFIGURACAO = "EM_CONFIGURACAO", "Em configuração"
    CONFIGURADO = "CONFIGURADO", "Configurado"


# =======
# chamado
# =======
class Chamado(models.Model):
    class Status(models.TextChoices):
        EM_ABERTURA = "EM_ABERTURA", "Em abertura"
        ABERTO = "ABERTO", "Aberto"
        EM_EXECUCAO = "EM_EXECUCAO", "Em execução"
        AGUARDANDO_NF = "AGUARDANDO_NF", "Aguardando NF"
        AGUARDANDO_COLETA = "AGUARDANDO_COLETA", "Aguardando coleta"
        FINALIZADO = "FINALIZADO", "Finalizado"

    class Tipo(models.TextChoices):
        ENVIO = "ENVIO", "Envio (Matriz → Loja)"
        RETORNO = "RETORNO", "Retorno (Loja → Matriz)"

    class Prioridade(models.TextChoices):
        MAIS_ANTIGO = "MAIS_ANTIGO", "Mais antigo (padrão)"
        BAIXA = "BAIXA", "Baixa"
        MEDIA = "MEDIA", "Média"
        ALTA = "ALTA", "Alta"
        CRITICA = "CRITICA", "Crítica"

    loja = models.ForeignKey(Loja, on_delete=models.PROTECT)
    projeto = models.ForeignKey(Projeto, on_delete=models.PROTECT)
    subprojeto = models.ForeignKey(Subprojeto, on_delete=models.PROTECT)
    kit = models.ForeignKey(Kit, on_delete=models.PROTECT)

    tipo = models.CharField(max_length=20, choices=Tipo.choices, default=Tipo.ENVIO)

    chamado_origem = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="retornos",
        help_text="Chamado de origem (obrigatório quando tipo=RETORNO).",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.EM_ABERTURA,
        db_index=True,
    )
    prioridade = models.CharField(
        max_length=20,
        choices=Prioridade.choices,
        default=Prioridade.MAIS_ANTIGO,
        db_index=True,
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    finalizado_em = models.DateTimeField(null=True, blank=True)
    protocolo = models.CharField(max_length=32, unique=True, editable=False)

    # =========================
    # Ticket externo (novo)
    # =========================
    # NOTA: deixar blank/default na migration inicial para não quebrar dados existentes.
    # A obrigatoriedade real fica na UI (form) + migração de endurecimento depois.
    ticket_externo_sistema = models.CharField(max_length=50, blank=True, default="")
    ticket_externo_id = models.CharField(max_length=50, blank=True, default="")

    # =========================
    # Coleta (novo gate ENVIO)
    # =========================
    coleta_confirmada_em = models.DateTimeField(null=True, blank=True)

    # =========================
    # Legado / compatibilidade
    # =========================
    # manter por enquanto para não quebrar templates/tests/DB;
    # depois migraremos para ticket_externo_* e removeremos.
    servicenow_numero = models.CharField(max_length=40, unique=True, null=True, blank=True)

    # Administrativo/financeiro (já existia)
    contabilidade_numero = models.CharField(max_length=40, unique=True, null=True, blank=True)
    nf_saida_numero = models.CharField(max_length=40, unique=True, null=True, blank=True)

    def __str__(self) -> str:
        return self.protocolo or f"Chamado {self.pk}"

    def clean(self) -> None:
        super().clean()

        # Subprojeto pode ser opcional na UI dependendo do cadastro.
        # Se o model estiver como PROTECT (obrigatório), manter.
        # Caso vocês decidam tornar Subprojeto opcional no futuro, este método já é compatível.
        if self.tipo == self.Tipo.RETORNO:
            if not self.chamado_origem_id:
                raise ValidationError(
                    {"chamado_origem": "Chamado de retorno exige um chamado de origem."}
                )

            if self.pk and self.chamado_origem_id == self.pk:
                raise ValidationError(
                    {"chamado_origem": "Chamado não pode ser origem de si mesmo."}
                )

            origem = self.chamado_origem
            if origem and origem.status != self.Status.FINALIZADO:
                raise ValidationError(
                    {"chamado_origem": "Chamado de origem deve estar FINALIZADO."}
                )

        else:
            if self.chamado_origem_id:
                raise ValidationError(
                    {"chamado_origem": "Chamado de envio não deve possuir chamado de origem."}
                )

    # -------------------------
    # geração de itens do chamado
    # -------------------------
    def gerar_itens_de_instalacao(self) -> None:
        """
        Gera itens do chamado a partir do kit.
        - Itens rastreáveis (equipamento.tem_ativo=True): explode em linhas unitárias para bipagem.
        - Itens contáveis (equipamento.tem_ativo=False): cria linha agregada com quantidade.

        Deve ser idempotente: se já existem itens, não cria novamente.
        """
        if self.itens.exists():
            return

        for item_kit in self.kit.itens.select_related("equipamento").all():
            eq = item_kit.equipamento

            if eq.tem_ativo:
                for _ in range(item_kit.quantidade):
                    InstalacaoItem.objects.create(
                        chamado=self,
                        equipamento=eq,
                        tipo=str(item_kit.tipo),
                        quantidade=1,
                        tem_ativo=True,
                        requer_configuracao=item_kit.requer_configuracao,
                    )
            else:
                InstalacaoItem.objects.create(
                    chamado=self,
                    equipamento=eq,
                    tipo=str(item_kit.tipo),
                    quantidade=item_kit.quantidade,
                    tem_ativo=False,
                    requer_configuracao=item_kit.requer_configuracao,
                )

    def pode_liberar_nf(self) -> bool:
        """
        Gate de NF (ENVIO):
        - precisa ter itens gerados
        - todo item rastreável (tem_ativo=True) deve ter ativo + numero_serie
        - todo item contável (tem_ativo=False) deve estar confirmado
        Configuração (IP) NÃO entra neste gate.
        """
        if self.tipo != self.Tipo.ENVIO:
            return False

        qs = self.itens.all()
        if not qs.exists():
            return False

        for item in qs:
            if item.tem_ativo:
                if not (item.ativo or "").strip() or not (item.numero_serie or "").strip():
                    return False
            else:
                if not item.confirmado:
                    return False

        return True

    # ----------
    # finalizar
    # ----------
    def finalizar(self) -> None:
        """
        Finaliza o chamado aplicando regras de validação.

        ENVIO:
        - Itens rastreáveis: exige ativo + número de série.
        - Itens contáveis: exige confirmado=True.
        - Configuração: EXIGIDA APENAS quando item.deve_configurar=True
          exigindo:
            - status_configuracao=CONFIGURADO
            - ip preenchido
        - NF de saída é obrigatória (nf_saida_numero)
        - Coleta confirmada é obrigatória (coleta_confirmada_em)

        RETORNO:
        - Exige desfecho (status_retorno).
        - NAO_RETORNADO exige motivo.
        - RETORNADO rastreável exige ativo + número de série.
        """
        if self.status == self.Status.FINALIZADO:
            raise ValidationError("Chamado já está finalizado.")

        itens = list(self.itens.all())
        if not itens:
            raise ValidationError("Não é possível finalizar um chamado sem itens.")

        erros: list[str] = []

        # ==========================
        # ENVIO (Matriz -> Loja)
        # ==========================
        if self.tipo == self.Tipo.ENVIO:
            if not (self.nf_saida_numero or "").strip():
                erros.append("Não é possível finalizar: informe a NF de saída.")

            if self.coleta_confirmada_em is None:
                erros.append("Não é possível finalizar: confirme a coleta pela transportadora.")

            for item in itens:
                if item.deve_configurar:
                    if item.status_configuracao != StatusConfiguracao.CONFIGURADO:
                        erros.append(
                            "Não é possível finalizar: "
                            f"'{item.equipamento.nome} {item.tipo}' ainda não foi marcado como "
                            "CONFIGURADO."
                        )
                    if not item.ip:
                        erros.append(
                            "Não é possível finalizar: "
                            f"'{item.equipamento.nome} {item.tipo}' exige IP (configuração)."
                        )

                if item.tem_ativo:
                    if not (item.ativo or "").strip() or not (item.numero_serie or "").strip():
                        erros.append(
                            "Item rastreável "
                            f"'{item.equipamento.nome} {item.tipo}' "
                            "exige Ativo e Número de Série."
                        )
                else:
                    if not item.confirmado:
                        erros.append(
                            f"Item contável '{item.equipamento.nome} {item.tipo}' "
                            "precisa ser confirmado."
                        )

        # ==========================
        # RETORNO (Loja -> Matriz)
        # ==========================
        elif self.tipo == self.Tipo.RETORNO:
            for item in itens:
                if not item.status_retorno:
                    erros.append(
                        f"Defina o desfecho de retorno para '{item.equipamento.nome} {item.tipo}'."
                    )
                    continue

                if item.status_retorno == item.StatusRetorno.NAO_RETORNADO:
                    if not (item.motivo_nao_retorno or "").strip():
                        erros.append(
                            "Informe o motivo do não retorno para "
                            f"'{item.equipamento.nome} {item.tipo}'."
                        )
                    continue

                if item.status_retorno == item.StatusRetorno.RETORNADO:
                    if item.tem_ativo:
                        if not (item.ativo or "").strip() or not (item.numero_serie or "").strip():
                            erros.append(
                                "Item rastreável retornado "
                                f"'{item.equipamento.nome} {item.tipo}' "
                                "exige Ativo e Número de Série."
                            )

        else:
            erros.append(f"Tipo de chamado inválido: {self.tipo}")

        if erros:
            raise ValidationError(erros)

        self.status = self.Status.FINALIZADO
        self.finalizado_em = timezone.now()
        self.save(update_fields=["status", "finalizado_em"])

    # -----------------------
    # salvar / gerar protocolo
    # -----------------------
    def save(self, *args, **kwargs):  # type: ignore[override]
        if self.protocolo:
            return super().save(*args, **kwargs)

        data = timezone.now().strftime("%Y%m%d")

        for _ in range(5):
            self.protocolo = f"EX360-{data}-{secrets.token_hex(3).upper()}"
            try:
                with transaction.atomic():
                    return super().save(*args, **kwargs)
            except IntegrityError:
                self.protocolo = ""

        return super().save(*args, **kwargs)


# ================
# item da instalação
# ================
class InstalacaoItem(models.Model):
    class StatusRetorno(models.TextChoices):
        RETORNADO = "RETORNADO", "Retornado"
        NAO_RETORNADO = "NAO_RETORNADO", "Não retornado"

    chamado = models.ForeignKey(Chamado, on_delete=models.CASCADE, related_name="itens")
    equipamento = models.ForeignKey(Equipamento, on_delete=models.PROTECT)

    tipo = models.CharField(max_length=80)
    quantidade = models.PositiveIntegerField()

    tem_ativo = models.BooleanField()
    confirmado = models.BooleanField(default=False)

    # compatibilidade com o kit (pode virar "sugere_configuracao" no futuro)
    requer_configuracao = models.BooleanField(
        default=False,
        help_text="(Compat) Informação vinda do kit. A obrigatoriedade é decidida no chamado.",
    )

    # decisão do chamado
    deve_configurar = models.BooleanField(
        default=False,
        help_text="Decisão do chamado: este item deve ser configurado?",
    )

    # IP (somente quando deve_configurar=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    status_configuracao = models.CharField(
        max_length=20,
        choices=StatusConfiguracao.choices,
        default=StatusConfiguracao.AGUARDANDO,
        help_text="Estado atual do processo de configuração do item.",
    )

    ativo = models.CharField(max_length=80, blank=True, default="")
    numero_serie = models.CharField(max_length=120, blank=True, default="")

    status_retorno = models.CharField(
        max_length=20,
        choices=StatusRetorno.choices,
        null=True,
        blank=True,
        default=None,
        help_text="Obrigatório para itens em Chamado do tipo RETORNO.",
    )

    motivo_nao_retorno = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="Obrigatório quando status_retorno=NAO_RETORNADO.",
    )

    class Meta:
        verbose_name = "Item de Instalação"
        verbose_name_plural = "Itens de Instalação"

    def __str__(self) -> str:
        return f"{self.equipamento.nome} {self.tipo} ({self.quantidade})"


class ItemConfiguracaoLog(models.Model):
    item = models.ForeignKey(
        "InstalacaoItem",
        on_delete=models.CASCADE,
        related_name="logs_configuracao",
    )
    de_status = models.CharField(max_length=20, choices=StatusConfiguracao.choices)
    para_status = models.CharField(max_length=20, choices=StatusConfiguracao.choices)

    motivo = models.CharField(max_length=255, blank=True, default="")
    criado_em = models.DateTimeField(auto_now_add=True)

    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="logs_configuracao_criados",
    )

    class Meta:
        ordering = ["-criado_em", "-id"]

    def __str__(self) -> str:
        return f"{self.item_id}: {self.de_status} -> {self.para_status}"


# ==================
# evidências do chamado
# ==================
class EvidenciaChamado(models.Model):
    class Tipo(models.TextChoices):
        NF_SAIDA = "NF_SAIDA", "NF Saída"
        NF_RETORNO = "NF_RETORNO", "NF Retorno"
        CARTA_CONTEUDO = "CARTA_CONTEUDO", "Carta de Conteúdo"
        EXCECAO = "EXCECAO", "Exceção"
        OUTRO = "OUTRO", "Outro"

    chamado = models.ForeignKey(Chamado, on_delete=models.CASCADE, related_name="evidencias")
    tipo = models.CharField(max_length=30, choices=Tipo.choices)
    arquivo = models.FileField(upload_to="execucao/evidencias/")
    descricao = models.CharField(max_length=255, blank=True, default="")
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criado_em", "-id"]

    def __str__(self) -> str:
        return f"{self.get_tipo_display()} - {self.chamado.protocolo}"
