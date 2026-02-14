# web/execucao/admin.py
from django.contrib import admin
from .models import ExecutionSession, ExecutionSessionLog


@admin.register(ExecutionSession)
class ExecutionSessionAdmin(admin.ModelAdmin):
    list_display = (
        "chamado",
        "usuario",
        "started_at",
        "expires_at",
        "ended_at",
        "ended_reason",
    )
    list_filter = ("ended_reason",)
    search_fields = ("chamado__protocolo", "usuario__username")


@admin.register(ExecutionSessionLog)
class ExecutionSessionLogAdmin(admin.ModelAdmin):
    list_display = (
        "chamado",
        "previous_usuario",
        "new_usuario",
        "reason",
        "created_at",
    )
    list_filter = ("reason",)
