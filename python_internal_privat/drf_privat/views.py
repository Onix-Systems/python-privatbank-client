from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Privat
from .serializers import (
    PrivatSerializer,
    PrivatPaymentSerializer,
    PrivatPeriodSerializer,
)
from .exceptions import (
    PrivatDoesNotExistsException,
    PrivatExistsException,
)

from sync_privat.manager import SyncPrivatManager

mng = SyncPrivatManager


class PrivatView(GenericAPIView):
    serializer_class = PrivatSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        _ = serializer.validated_data
        privat_obj = Privat.objects.filter(user=request.user)
        if privat_obj.first() is not None:
            raise PrivatExistsException
        privat_obj.create(
            privat_token=_["privat_token"],
            iban_UAH=_["iban_UAH"],
            user=self.request.user,
        )
        return Response(
            {"detail": "Privatbank credentials added successfully."},
            status.HTTP_201_CREATED,
        )

    def put(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        _ = serializer.validated_data
        privat_obj = Privat.objects.filter(user=request.user)
        if privat_obj.first() is not None:
            privat_obj.update(privat_token=_["privat_token"], iban_UAH=_["iban_UAH"])
            return Response({"detail": "Privatbank credentials changed successfully."})
        raise PrivatDoesNotExistsException

    def delete(self, request):
        privat_obj = Privat.objects.filter(user=request.user)
        if privat_obj.first() is not None:
            privat_obj.delete()
            return Response(status.HTTP_204_NO_CONTENT)
        raise PrivatDoesNotExistsException


class PrivatCurrenciesCashRate(APIView):
    def get(self, request):
        response = mng.get_currencies(cashe_rate=True)
        return Response(response)


class PrivatCurrenciesNonCashRate(APIView):
    def get(self, request):
        response = mng.get_currencies(cashe_rate=False)
        return Response(response)


class PrivatClientInfo(APIView):
    def get(self, request):
        privat_obj = Privat.objects.filter(user=request.user).first()
        if privat_obj is not None:
            mng = SyncPrivatManager(privat_obj.privat_token, privat_obj.iban_UAH)
            response = mng.get_client_info()
            return Response(response)
        raise PrivatDoesNotExistsException


class PrivatBalanceView(APIView):
    def get(self, request):
        privat_obj = Privat.objects.filter(user=request.user).first()
        if privat_obj is not None:
            mng = SyncPrivatManager(privat_obj.privat_token, privat_obj.iban_UAH)
            response = mng.get_balance()
            return Response(response)
        raise PrivatDoesNotExistsException


class PrivatStatementView(GenericAPIView):
    serializer_class = PrivatPeriodSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        _ = serializer.validated_data
        privat_obj = Privat.objects.filter(user=request.user).first()
        if privat_obj is not None:
            mng = SyncPrivatManager(privat_obj.privat_token, privat_obj.iban_UAH)
            period = _["period"]
            limit = _["limit"]
            response = mng.get_statement(period, limit)
            return Response(response)
        raise PrivatDoesNotExistsException


class PrivatPaymentView(GenericAPIView):
    serializer_class = PrivatPaymentSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        _ = serializer.validated_data
        privat_obj = Privat.objects.filter(user=request.user).first()
        if privat_obj is not None:
            mng = SyncPrivatManager(privat_obj.privat_token, privat_obj.iban_UAH)
            response = mng.create_payment(_["recipient"], str(_["amount"]))
            return Response(response)
        raise PrivatDoesNotExistsException
