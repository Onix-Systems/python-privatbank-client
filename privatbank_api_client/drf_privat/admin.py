from django.contrib import admin
from .models import Privat


@admin.register(Privat)
class MonoAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "privat_token",
        "iban_UAH",
        "date_joined",
    )
