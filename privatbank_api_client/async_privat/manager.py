import json
import aiohttp
from typing import Dict
from privatbank_api_client.privat_config.manager import BasePrivatManager


class AsyncPrivatManager(BasePrivatManager):
    """
    A manager class providing asynchronous methods to interact with Privat APIs,
    inheriting shared utilities from BasePrivatManager.

    This class is responsible for making HTTP requests to the Privat APIs and
    supports methods to get currency rates, balance, transaction statements, and
    create payments.
    """

    @classmethod
    async def session(cls) -> aiohttp.client.ClientSession:
        """
        Creates and returns an async `aiohttp.ClientSession` object.

        :return: An instance of `aiohttp.ClientSession`.
        :rtype: aiohttp.client.ClientSession
        """
        return aiohttp.ClientSession()

    async def async_request(

        self, method: str, uri: str, headers=None, data=None
    ) -> Dict:
        """
        Sends an asynchronous HTTP request to the given URI
        :param method: The HTTP method to use (e.g., "GET", "POST").
        :type method: str
        :param uri: The target API endpoint.
        :type uri: str
        :param headers: Optional HTTP headers to send with the request.
        :type headers: dict or None
        :param data: Optional payload for POST requests.
        :type data: dict or None
        :return: A dictionary containing the response payload.
        :rtype: dict
        :raises aiohttp.ClientResponseError: If the request results in an HTTP error.
        :raises Exception: For other unexpected exceptions.
        """
        session = await self.session()
        if method == "GET":
            response = await session.get(uri, headers=headers)
        if method == "POST":
            response = await session.post(uri, headers=headers, data=data)
        try:
            code = response.status
            response.raise_for_status()
            detail = await response.json()
            payload = self.privat_response(code, detail)
            return payload
        except aiohttp.ClientResponseError as exc:
            error_response = self.privat_response(code, str(exc.message))
            return error_response
        except Exception as exc:
            exception = {"detail": str(exc)}
            return exception

    async def get_currencies(self, cashe_rate: bool) -> Dict:
        """
        Fetches currency rates from the Privat APIs.

        :param cashe_rate: Determines whether to fetch cash rate or non-cash rate.
        :type cashe_rate: bool
        :return: A dictionary with currency rate data.
        :rtype: dict
        :raises Exception: If an error occurs during the request.
        """
        try:
            if cashe_rate:
                uri = self.privat_currencies_cashe_rate_uri
            else:
                uri = self.privat_currencies_non_cashe_rate_uri
            response = await self.async_request(method="GET", uri=uri)
            return response
        except Exception as exc:
            exception = {"detail": str(exc)}
            return exception

    async def get_client_info(self) -> Dict:
        """
        Retrieves detailed client information from Privat APIs.

        :return: A dictionary containing client information details.
        :rtype: dict
        :raises Exception: If an error occurs during the request.
        """
        try:
            token = self.token
            iban = self.iban
            date = self.date(0).get("date")
            balance_uri = self.privat_balance_uri
            uri_body = self.privat_balance_uri_body
            uri = uri_body.format(balance_uri, iban, date)
            headers = {"token": token}
            response = await self.async_request(method="GET", uri=uri, headers=headers)
            return response
        except Exception as exc:
            exception = {"detail": str(exc)}
            return exception

    async def get_balance(self) -> Dict:
        """
        Retrieves the account balance for the authorized client.

        :return: A dictionary containing the account balance details.
        :rtype: dict
        :raises Exception: If there's an error retrieving or parsing the balance data.
        """
        try:
            payload = await self.get_client_info()
            code = payload.get("code")
            data = payload.get("detail")
            balance = {"balance": data["balances"][0]["balanceOutEq"]}
            response = self.privat_response(code, balance)
            return response
        except Exception:
            return payload

    async def get_statement(self, period: int, limit: int) -> Dict:
        """
        Fetches the transaction statement for a specified time period and limit.

        :param period: The period in days to retrieve transactions for.
        :type period: int
        :param limit: The maximum number of transactions to retrieve.
        :type limit: int
        :return: A dictionary of transaction statement details.
        :rtype: dict
        :raises Exception: If an error occurs during the request.
        """
        try:
            token = self.token
            iban = self.iban
            statement_uri = self.privat_statement_uri
            uri_body = self.privat_statement_uri_body
            date = self.date(period).get("date")
            uri = uri_body.format(statement_uri, iban, date, limit)
            headers = {"token": token}
            response = await self.async_request(method="GET", uri=uri, headers=headers)
            return response
        except Exception as exc:
            exception = {"detail": str(exc)}
            return exception

    async def create_payment(self, recipient: str, amount: float) -> Dict:
        """
        Creates a payment transaction using the Privat APIs.

        :param recipient: The recipient's identifier for the transaction.
        :type recipient: str
        :param amount: The amount to transfer.
        :type amount: float
        :return: A dictionary containing the status or result of the payment.
        :rtype: dict
        :raises Exception: If an error occurs during the request.
        """
        try:
            token = self.token
            iban = self.iban
            payment_body = self.payment_body(recipient, amount, iban)
            data = json.dumps(payment_body)
            headers = {"token": token}
            uri = self.privat_payment_uri
            response = await self.async_request(
                method="POST", uri=uri, headers=headers, data=data
            )
            return response
        except Exception as exc:
            exception = {"detail": str(exc)}
            return exception
