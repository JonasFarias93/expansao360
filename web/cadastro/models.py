# Create your models here.
from django.db import models


class Loja(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nome = models.CharField(max_length=120)

    class Meta:
        verbose_name = "Loja"
        verbose_name_plural = "Lojas"

    def __str__(self) -> str:
        return f"{self.codigo} - {self.nome}"


class Kit(models.Model):
    nome = models.CharField(max_length=120, unique=True)

    class Meta:
        verbose_name = "Kit"
        verbose_name_plural = "Kits"

    def __str__(self) -> str:
        return self.nome


class ItemKit(models.Model):
    kit = models.ForeignKey(Kit, on_delete=models.CASCADE, related_name="itens")
    nome = models.CharField(max_length=120)
    quantidade = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Item do Kit"
        verbose_name_plural = "Itens do Kit"
        unique_together = ("kit", "nome")

    def __str__(self) -> str:
        return f"{self.nome} ({self.quantidade})"
