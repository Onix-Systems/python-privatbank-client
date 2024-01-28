from rest_framework import serializers
from .models import Privat


class PrivatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Privat
        fields = ["privat_token", "iban_UAH"]
        extra_kwargs = {"privat_token": {"write_only": True}}


class PrivatPaymentSerializer(serializers.Serializer):
    amount = serializers.FloatField(min_value=0.01)
    recipient = serializers.CharField(max_length=16)


class PrivatPeriodSerializer(serializers.Serializer):
    period = serializers.IntegerField(min_value=0)
    limit = serializers.IntegerField(default=100, min_value=0, max_value=500)
