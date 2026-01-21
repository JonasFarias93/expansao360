# Register your models here.
from django.contrib import admin

from .models import ItemKit, Kit, Loja


@admin.register(Loja)
class LojaAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nome")
    search_fields = ("codigo", "nome")


class ItemKitInline(admin.TabularInline):
    model = ItemKit
    extra = 1


@admin.register(Kit)
class KitAdmin(admin.ModelAdmin):
    list_display = ("nome",)
    search_fields = ("nome",)
    inlines = [ItemKitInline]
