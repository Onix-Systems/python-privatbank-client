from typing import Dict
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Privat
from .serializers import (
    PrivatSerializer,
    PrivatPaymentSerializer,
    PrivatPeriodSerializer,
)
from sync_privat.manager import SyncPrivatManager


class PrivatView(GenericAPIView):
    serializer_class = PrivatSerializer

    def post(self, request) -> Dict:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        _ = serializer.validated_data
        privat = Privat.objects.filter(user=request.user)
        mng = SyncPrivatManager()
        if privat.first() is not None:
            response = mng.exists_exception()
        else:
            privat.create(
                privat_token=_["privat_token"],
                iban_UAH=_["iban_UAH"],
                user=self.request.user,
            )
            response = mng.create_success()
        return Response(response)

    def put(self, request) -> Dict:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        _ = serializer.validated_data
        privat = Privat.objects.filter(user=request.user)
        mng = SyncPrivatManager()
        if privat.first() is not None:
            privat.update(privat_token=_["privat_token"], iban_UAH=_["iban_UAH"])
            response = mng.update_success()
        else:
            response = mng.does_not_exsists_exception()
        return Response(response)

    def delete(self, request) -> Dict:
        privat = Privat.objects.filter(user=request.user)
        mng = SyncPrivatManager()
        if privat.first() is not None:
            privat.delete()
            response = mng.delete_success()
        else:
            response = mng.does_not_exsists_exception()
        return Response(response)


class PrivatCurrenciesCashRate(APIView):
    def get(self, request) -> Dict:
        mng = SyncPrivatManager()
        response = mng.get_currencies(cashe_rate=True)
        return Response(response)


class PrivatCurrenciesNonCashRate(APIView):
    def get(self, request) -> Dict:
        mng = SyncPrivatManager()
        response = mng.get_currencies(cashe_rate=False)
        return Response(response)


class PrivatClientInfo(APIView):
    def get(self, request) -> Dict:
        privat = Privat.objects.filter(user=request.user).first()
        mng = SyncPrivatManager()
        if privat is not None:
            mng.token = privat.privat_token
            mng.iban = privat.iban_UAH
            response = mng.get_client_info()
        else:
            response = mng.does_not_exsists_exception()
        return Response(response)


class PrivatBalanceView(APIView):
    def get(self, request) -> Dict:
        privat = Privat.objects.filter(user=request.user).first()
        mng = SyncPrivatManager()
        if privat is not None:
            mng.token = privat.privat_token
            mng.iban = privat.iban_UAH
            response = mng.get_balance()
        else:
            response = mng.does_not_exsists_exception()
        return Response(response)


class PrivatStatementView(GenericAPIView):
    serializer_class = PrivatPeriodSerializer

    def post(self, request) -> Dict:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        _ = serializer.validated_data
        privat = Privat.objects.filter(user=request.user).first()
        mng = SyncPrivatManager()
        if privat is not None:
            mng.token = privat.privat_token
            mng.iban = privat.iban_UAH
            period = _["period"]
            limit = _["limit"]
            response = mng.get_statement(period, limit)
        else:
            response = mng.does_not_exsists_exception()
        return Response(response)


class PrivatPaymentView(GenericAPIView):
    serializer_class = PrivatPaymentSerializer

    def post(self, request) -> Dict:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        _ = serializer.validated_data
        privat = Privat.objects.filter(user=request.user).first()
        mng = SyncPrivatManager()
        if privat is not None:
            mng.token = privat.privat_token
            mng.iban = privat.iban_UAH
            response = mng.create_payment(_["recipient"], str(_["amount"]))
        else:
            response = mng.does_not_exsists_exception()
        return Response(response)
