import json
import requests
from typing import Dict
from privatbank_api_client.privat_config.manager import BasePrivatManager


class SyncPrivatManager(BasePrivatManager):
    """
    SyncPrivatManager provides methods to interact with PrivatBank APIs synchronously.
    The class is used for retrieving account information, balances, making payments,
    and obtaining transaction statements.
    """

    @classmethod
    def session(cls) -> requests.sessions.Session:
        """
        Create and return a session object for making HTTP requests.

        :return: A new requests.Session instance.
        :rtype: requests.sessions.Session
        """
        return requests.Session()

    def sync_request(
            self,
            method: str,
            uri: str,
            headers=None,
            data=None,
    ) -> Dict:
        """
            Perform a synchronous HTTP request using the specified method, URI, headers, and data
            :param method: HTTP method for the request (e.g., "GET", "POST").
            :type method: str
            :param uri: The URI to which the request is sent.
            :type uri: str
            :param headers: Optional headers to include in the request.
            :type headers: dict or None
            :param data: Optional data payload for POST requests.
            :type data: dict, str, bytes, or None
            :return: The response from the server parsed into a dictionary.
            :rtype: dict
            """
        session = self.session()
        if method == "GET":
            response = session.get(uri, headers=headers)
        if method == "POST":
            response = session.post(uri, headers=headers, data=data)
        try:
            code = response.status_code
            response.raise_for_status()
            detail = response.json()
            payload = self.privat_response(code, detail)
            return payload
        except requests.exceptions.HTTPError as exc:
            error_response = self.privat_response(code, str(exc))
            return error_response
        except Exception as exc:
            exception = {"detail": str(exc)}
            return exception

    def get_currencies(self, cashe_rate: bool) -> Dict:
        """
        Obtain exchange rates from PrivatBank APIs.

        :param cashe_rate: Whether to fetch cash exchange rates.
        :type cashe_rate: bool
        :return: A dictionary containing exchange rate information.
        :rtype: dict
        """
        try:
            if cashe_rate:
                uri = self.privat_currencies_cashe_rate_uri
            else:
                uri = self.privat_currencies_non_cashe_rate_uri
            response = self.sync_request(method="GET", uri=uri)
            return response
        except Exception as exc:
            exception = {"detail": str(exc)}
            return exception

    def get_client_info(self) -> Dict:
        """
        Retrieve client account information (e.g., balances or transactions).

        :return: A dictionary comprising client details from PrivatBank.
        :rtype: dict
        """
        try:
            token = self.token
            iban = self.iban
            date = self.date(0).get("date")
            balance_uri = self.privat_balance_uri
            uri_body = self.privat_balance_uri_body
            uri = uri_body.format(balance_uri, iban, date)
            headers = {"token": token}
            response = self.sync_request(method="GET", uri=uri, headers=headers)
            return response
        except Exception as exc:
            exception = {"detail": str(exc)}
            return exception

    def get_balance(self) -> Dict:
        """
        Retrieve the account balance from the client information.

        :return: A dictionary containing the account balance.
        :rtype: dict
        """
        try:
            payload = self.get_client_info()
            code = payload.get("code")
            data = payload.get("detail")
            balance = {"balance": data["balances"][0]["balanceOutEq"]}
            response = self.privat_response(code, balance)
            return response
        except Exception:
            return payload

    def get_statement(self, period: int, limit: int) -> Dict:
        """
        Retrieve the account statement for a given period and limit.

        :param period: The number of days prior to the current date for which to fetch transactions.
        :type period: int
        :param limit: The maximum number of transactions to fetch.
        :type limit: int
        :return: A dictionary containing the statement details.
        :rtype: dict
        """
        try:
            token = self.token
            iban = self.iban
            statement_uri = self.privat_statement_uri
            uri_body = self.privat_statement_uri_body
            date = self.date(period).get("date")
            uri = uri_body.format(statement_uri, iban, date, limit)
            headers = {"token": token}
            response = self.sync_request(method="GET", uri=uri, headers=headers)
            return response
        except Exception as exc:
            exception = {"detail": str(exc)}
            return exception

    def create_payment(self, recipient: str, amount: float) -> Dict:
        """
        Create a payment transaction to a specified recipient.

        :param recipient: The recipient's account identifier.
        :type recipient: str
        :param amount: The amount to be transferred.
        :type amount: float
        :return: A dictionary denoting the payment response from the server.
        :rtype: dict
        """
        try:
            token = self.token
            iban = self.iban
            payment_body = self.payment_body(recipient, amount, iban)
            uri = self.privat_payment_uri
            headers = {"token": token}
            data = json.dumps(payment_body)
            response = self.sync_request(
                method="POST", uri=uri, headers=headers, data=data
            )
            return response
        except Exception as exc:
            exception = {"detail": str(exc)}
            return exception
