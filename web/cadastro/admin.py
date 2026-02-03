from django.contrib import admin

from .models import (
    Categoria,
    Equipamento,
    ItemKit,
    Kit,
    Loja,
    Projeto,
    Subprojeto,
    TipoEquipamento,
)


class TipoEquipamentoInline(admin.TabularInline):
    model = TipoEquipamento
    extra = 1


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    search_fields = ("nome",)
    inlines = [TipoEquipamentoInline]


@admin.register(TipoEquipamento)
class TipoEquipamentoAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nome", "categoria", "ativo")
    list_filter = ("categoria", "ativo")
    search_fields = ("codigo", "nome", "categoria__nome")


@admin.register(Equipamento)
class EquipamentoAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nome", "categoria", "tem_ativo", "configuravel")
    list_filter = ("categoria", "tem_ativo", "configuravel")
    search_fields = ("codigo", "nome", "categoria__nome")


@admin.register(Loja)
class LojaAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nome", "cidade", "uf", "logomarca")
    list_filter = ("uf", "logomarca")
    search_fields = ("codigo", "nome", "cidade")


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
    fields = ("equipamento", "tipo", "quantidade", "requer_configuracao")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "tipo":
            kwargs["queryset"] = TipoEquipamento.objects.filter(ativo=True).order_by(
                "categoria__nome", "nome"
            )
        if db_field.name == "equipamento":
            kwargs["queryset"] = Equipamento.objects.order_by("categoria__nome", "nome")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Kit)
class KitAdmin(admin.ModelAdmin):
    list_display = ("nome",)
    search_fields = ("nome",)
    inlines = [ItemKitInline]
