import json
import requests
from typing import Dict
from privat_config.manager import BasePrivatManager


class SyncPrivatManager(BasePrivatManager):
    @classmethod
    def session(cls) -> requests.sessions.Session:
        return requests.Session()

    def sync_request(
        self,
        method: str,
        uri: str,
        headers=None,
        data=None,
    ) -> Dict:
        session = self.session()
        if method == "GET":
            response = session.get(uri, headers=headers)
        if method == "POST":
            response = session.post(uri, headers=headers, data=data)
        try:
            code = response.status_code
            response.raise_for_status()
            response = {"code": code, "detail": response.json()}
            return response
        except requests.exceptions.HTTPError as exc:
            error_response = {"code": code, "detail": str(exc)}
            return error_response
        except Exception as exc:
            exception = {"detail": str(exc)}
            return exception

    def get_currencies(self, cashe_rate: bool) -> Dict:
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
        try:
            client_info = self.get_client_info()
            code = client_info.get("code")
            payload = client_info.get("detail")
            balance = {"code": code, "balance": payload["balances"][0]["balanceOutEq"]}
            return balance
        except Exception:
            return client_info

    def get_statement(self, period: int, limit: int) -> Dict:
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
