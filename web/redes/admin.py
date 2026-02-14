from django.contrib import admin

from .models import PerfilRede, RegraRedeEquipamento


@admin.register(PerfilRede)
class PerfilRedeAdmin(admin.ModelAdmin):
    list_display = ("codigo", "tipo", "ativo", "descricao")
    list_filter = ("tipo", "ativo")
    search_fields = ("codigo", "descricao")
    ordering = ("codigo",)


@admin.register(RegraRedeEquipamento)
class RegraRedeEquipamentoAdmin(admin.ModelAdmin):
    list_display = ("codigo", "ip_policy", "perfil_rede", "descricao")
    list_filter = ("ip_policy", "perfil_rede")
    search_fields = ("codigo", "descricao", "perfil_rede__codigo")
    ordering = ("perfil_rede__codigo", "codigo")
