from cadastro.models import Equipamento, Kit, Loja, Projeto, Subprojeto
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Chamado(models.Model):
    class Status(models.TextChoices):
        ABERTO = "ABERTO", "Aberto"
        EM_EXECUCAO = "EM_EXECUCAO", "Em execução"
        FINALIZADO = "FINALIZADO", "Finalizado"

    loja = models.ForeignKey(Loja, on_delete=models.PROTECT)
    projeto = models.ForeignKey(Projeto, on_delete=models.PROTECT)
    subprojeto = models.ForeignKey(Subprojeto, on_delete=models.PROTECT)
    kit = models.ForeignKey(Kit, on_delete=models.PROTECT)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ABERTO)
    criado_em = models.DateTimeField(auto_now_add=True)
    finalizado_em = models.DateTimeField(null=True, blank=True)

    def gerar_itens_de_instalacao(self) -> None:
        if self.itens.exists():
            return

        for item_kit in self.kit.itens.select_related("equipamento").all():
            InstalacaoItem.objects.create(
                chamado=self,
                equipamento=item_kit.equipamento,
                tipo=item_kit.tipo,
                quantidade=item_kit.quantidade,
                tem_ativo=item_kit.equipamento.tem_ativo,
            )

    def finalizar(self) -> None:
        erros: list[str] = []

        for item in self.itens.all():
            if item.tem_ativo:
                if not item.ativo.strip() or not item.numero_serie.strip():
                    erros.append(
                        "Item rastreável "
                        f"'{item.equipamento.nome} {item.tipo}' "
                        "exige Ativo e Número de Série."
                    )
            else:
                if not item.confirmado:
                    erros.append(
                        "Item contável "
                        f"'{item.equipamento.nome} {item.tipo}' "
                        "precisa ser confirmado."
                    )

        if erros:
            raise ValidationError(erros)

        self.status = self.Status.FINALIZADO
        self.finalizado_em = timezone.now()
        self.save(update_fields=["status", "finalizado_em"])


class InstalacaoItem(models.Model):
    chamado = models.ForeignKey(Chamado, on_delete=models.CASCADE, related_name="itens")
    equipamento = models.ForeignKey(Equipamento, on_delete=models.PROTECT)
    tipo = models.CharField(max_length=80)
    quantidade = models.PositiveIntegerField()

    tem_ativo = models.BooleanField()

    confirmado = models.BooleanField(default=False)

    ativo = models.CharField(max_length=80, blank=True, default="")
    numero_serie = models.CharField(max_length=120, blank=True, default="")

    def __str__(self) -> str:
        return f"{self.equipamento.nome} {self.tipo} ({self.quantidade})"
