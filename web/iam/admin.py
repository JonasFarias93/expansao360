# Register your models here.
from __future__ import annotations

from django.contrib import admin

from .models import Capability, UserCapability


@admin.register(Capability)
class CapabilityAdmin(admin.ModelAdmin):
    list_display = ("code", "description", "created_at")
    search_fields = ("code", "description")
    ordering = ("code",)


@admin.register(UserCapability)
class UserCapabilityAdmin(admin.ModelAdmin):
    list_display = ("user", "capability", "created_at")
    list_filter = ("capability",)
    search_fields = ("user__username", "user__email", "capability__code")
    autocomplete_fields = ("user", "capability")
