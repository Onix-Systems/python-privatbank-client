from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class Privat(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=False,
        unique=True,
    )
    privat_token = models.CharField(
        max_length=292,
        blank=False,
        unique=True,
    )
    iban_UAH = models.CharField(
        max_length=29,
        blank=False,
        unique=True,
    )
    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.user.email
