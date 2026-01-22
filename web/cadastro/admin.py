from django.contrib import admin

from .models import (
    Categoria,
    Equipamento,
    ItemKit,
    Kit,
    Loja,
    Projeto,
    Subprojeto,
)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    search_fields = ("nome",)


@admin.register(Equipamento)
class EquipamentoAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nome", "categoria", "tem_ativo", "configuravel")
    list_filter = ("categoria", "tem_ativo", "configuravel")

    search_fields = ("codigo", "nome")


@admin.register(Loja)
class LojaAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nome")
    search_fields = ("codigo", "nome")


class SubprojetoInline(admin.TabularInline):
    model = Subprojeto
    extra = 1


@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nome")
    search_fields = ("codigo", "nome")
    inlines = [SubprojetoInline]


class ItemKitInline(admin.TabularInline):
    model = ItemKit
    extra = 0
    fields = (
        "equipamento",
        "tipo",
        "quantidade",
        "requer_configuracao",
    )


@admin.register(Kit)
class KitAdmin(admin.ModelAdmin):
    list_display = ("nome",)
    search_fields = ("nome",)
    inlines = [ItemKitInline]
