from django.db import models


class Categoria(models.Model):
    nome = models.CharField(max_length=80, unique=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self) -> str:
        return self.nome


class Equipamento(models.Model):
    codigo = models.CharField(max_length=50, unique=True)  # MICRO, MONITOR
    nome = models.CharField(max_length=120)  # Micro, Monitor
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="equipamentos")
    tem_ativo = models.BooleanField(default=True)
    configuravel = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Equipamento"
        verbose_name_plural = "Equipamentos"

    def __str__(self) -> str:
        return f"{self.nome} ({self.codigo})"


class Loja(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nome = models.CharField(max_length=120)

    class Meta:
        verbose_name = "Loja"
        verbose_name_plural = "Lojas"

    def __str__(self) -> str:
        return f"{self.codigo} - {self.nome}"


class Projeto(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nome = models.CharField(max_length=120)

    class Meta:
        verbose_name = "Projeto"
        verbose_name_plural = "Projetos"

    def __str__(self) -> str:
        return f"{self.codigo} - {self.nome}"


class Subprojeto(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name="subprojetos")
    codigo = models.CharField(max_length=50)
    nome = models.CharField(max_length=120)

    class Meta:
        verbose_name = "Subprojeto"
        verbose_name_plural = "Subprojetos"
        unique_together = ("projeto", "codigo")

    def __str__(self) -> str:
        return f"{self.projeto.codigo}/{self.codigo} - {self.nome}"


class Kit(models.Model):
    nome = models.CharField(max_length=120, unique=True)

    class Meta:
        verbose_name = "Kit"
        verbose_name_plural = "Kits"

    def __str__(self) -> str:
        return self.nome


class ItemKit(models.Model):
    kit = models.ForeignKey(Kit, on_delete=models.CASCADE, related_name="itens")
    equipamento = models.ForeignKey(Equipamento, on_delete=models.PROTECT)
    tipo = models.CharField(max_length=80)  # PDV, TOUCH, etc
    quantidade = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Item do Kit"
        verbose_name_plural = "Itens do Kit"
        unique_together = ("kit", "equipamento", "tipo")

    @property
    def nome_exibicao(self) -> str:
        return f"{self.equipamento.nome} {self.tipo}".strip()

    def __str__(self) -> str:
        return f"{self.nome_exibicao} ({self.quantidade})"
