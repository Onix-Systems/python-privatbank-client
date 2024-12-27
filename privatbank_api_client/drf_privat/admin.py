from django.contrib import admin
from privatbank_api_client.drf_privat.models import Privat


@admin.register(Privat)
class PrivatAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "privat_token",
        "iban_UAH",
        "date_joined",
    )
