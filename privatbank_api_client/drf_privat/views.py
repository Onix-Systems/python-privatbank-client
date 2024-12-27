from typing import Dict
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from privatbank_api_client.drf_privat.models import Privat
from privatbank_api_client.drf_privat.serializers import (
    PrivatSerializer,
    PrivatPaymentSerializer,
    PrivatPeriodSerializer,
)
from privatbank_api_client.sync_privat.manager import SyncPrivatManager


class PrivatView(GenericAPIView):
    """
    Handles CRUD operations for Privat model instances.

    Methods:
        post(request): Creates a new Privat instance for the user or raises an exception if one exists.
        put(request): Updates the existing Privat instance with new data or raises an exception if none exists.
        delete(request): Deletes the user's Privat instance or raises an exception if none exists.
    """
    serializer_class = PrivatSerializer

    def post(self, request) -> Dict:
        """
        Creates a new Privat instance for the user.

        :param request: The HTTP request containing user's data to create the Privat instance.
        :type request: Request
        :return: HTTP response indicating success or failure of the operation.
        :rtype: Dict
        """
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
        """
        Updates an existing Privat instance for the user.

        :param request: The HTTP request containing updated data for the Privat instance.
        :type request: Request
        :return: HTTP response indicating success or failure of the operation.
        :rtype: Dict
        """
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
        """
        Deletes the user's Privat instance.

        :param request: The HTTP request object.
        :type request: Request
        :return: HTTP response indicating success or failure of the deletion.
        :rtype: Dict
        """
        privat = Privat.objects.filter(user=request.user)
        mng = SyncPrivatManager()
        if privat.first() is not None:
            privat.delete()
            response = mng.delete_success()
        else:
            response = mng.does_not_exsists_exception()
        return Response(response)


class PrivatCurrenciesCashRate(APIView):
    """
    Retrieves cash currency rates from the Privat API.

    Methods:
        get(request): Fetches the cash currency rates.
    """

    def get(self, request) -> Dict:
        """
        Fetches cash currency rates.

        :param request: The HTTP request object.
        :type request: Request
        :return: HTTP response containing the cash currency rates.
        :rtype: Dict
        """
        mng = SyncPrivatManager()
        response = mng.get_currencies(cashe_rate=True)
        return Response(response)


class PrivatCurrenciesNonCashRate(APIView):
    """
    Retrieves non-cash currency rates from the Privat API.

    Methods:
        get(request): Fetches the non-cash currency rates.
    """

    def get(self, request) -> Dict:
        """
        Fetches non-cash currency rates.

        :param request: The HTTP request object.
        :type request: Request
        :return: HTTP response containing the non-cash currency rates.
        :rtype: Dict
        """
        mng = SyncPrivatManager()
        response = mng.get_currencies(cashe_rate=False)
        return Response(response)


class PrivatClientInfo(APIView):
    """
    Retrieves client information from the Privat API based on stored credentials.

    Methods:
        get(request): Fetches the client information.
    """

    def get(self, request) -> Dict:
        """
        Fetches client information from the Privat API.

        :param request: The HTTP request object.
        :type request: Request
        :return: HTTP response containing the client information.
        :rtype: Dict
        """
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
    """
    Retrieves account balance information from the Privat API.

    Methods:
        get(request): Fetches the account balance information.
    """

    def get(self, request) -> Dict:
        """
        Fetches account balance information for the user using the Privat API.

        :param request: The HTTP request object.
        :type request: Request
        :return: HTTP response containing the account balance.
        :rtype: Dict
        """
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
    """
    Retrieves account statements from the Privat API based on a given period and limit.

    Methods:
        post(request): Fetches account statements for the specified period and limit.
    """
    serializer_class = PrivatPeriodSerializer

    def post(self, request) -> Dict:
        """
        Fetches account statements based on the provided period and limit.

        :param request: The HTTP request containing the period and limit data.
        :type request: Request
        :return: HTTP response with the account statements or an error message.
        :rtype: Dict
        """
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
    """
    Handles payment operations through the Privat API.

    Methods:
        post(request): Processes and executes the payment based on provided recipient and amount.
    """
    serializer_class = PrivatPaymentSerializer

    def post(self, request) -> Dict:
        """
        Processes and executes a payment using the Privat API.

        :param request: The HTTP request containing payment details such as recipient and amount.
        :type request: Request
        :return: HTTP response indicating success or failure of the payment process.
        :rtype: Dict
        """
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
