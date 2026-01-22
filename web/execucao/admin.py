from django.contrib import admin

from .models import Chamado, InstalacaoItem


class InstalacaoItemInline(admin.TabularInline):
    model = InstalacaoItem
    extra = 0
    fields = (
        "equipamento",
        "tipo",
        "quantidade",
        "tem_ativo",
        "requer_configuracao",
        "status_configuracao",
        "confirmado",
        "ativo",
        "numero_serie",
    )
    readonly_fields = ("equipamento", "tipo", "quantidade", "tem_ativo")


@admin.register(Chamado)
class ChamadoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "protocolo",
        "servicenow_numero",
        "contabilidade_numero",
        "nf_saida_numero",
        "loja",
        "projeto",
        "subprojeto",
        "kit",
        "status",
        "criado_em",
        "finalizado_em",
    )
    list_filter = ("status", "projeto")
    search_fields = (
        "protocolo",
        "servicenow_numero",
        "contabilidade_numero",
        "nf_saida_numero",
        "loja__codigo",
        "loja__nome",
        "projeto__codigo",
        "projeto__nome",
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.gerar_itens_de_instalacao()


@admin.register(InstalacaoItem)
class InstalacaoItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "chamado",
        "equipamento",
        "tipo",
        "quantidade",
        "tem_ativo",
        "requer_configuracao",
        "status_configuracao",
        "confirmado",
    )
    list_filter = ("tem_ativo", "confirmado", "requer_configuracao", "status_configuracao")
    search_fields = ("ativo", "numero_serie", "equipamento__codigo", "equipamento__nome", "tipo")
