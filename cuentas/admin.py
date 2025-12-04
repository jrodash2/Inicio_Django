from django.contrib import admin

from .models import PerfilUsuario


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ("user", "actualizado_en")
    search_fields = ("user__username", "user__first_name", "user__last_name")
    autocomplete_fields = ["user"]
