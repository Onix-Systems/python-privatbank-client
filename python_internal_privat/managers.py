import json
import requests
from datetime import datetime
from typing import Any, Dict, Tuple

from .config import (
    PRIVATBANK_BALANCE_URI,
    PRIVATBANK_STATEMENT_URI,
    PRIVATBANK_PAYMENT_URI,
    PRIVATBANK_CURRENCY_CASHE_RATE_URI,
    PRIVATBANK_CURRENCY_NON_CASHE_RATE_URI,
    
    DOCUMENT_NUMBER,
    RECIPIENT_NCEO,
    PAYMENT_NAMING,
    RECIPIENT_IFI,
    RECIPIENT_IFI_TEXT,
    PAYMENT_DESTINATION,
    PAYMENT_CCY,
    DOCUMENT_TYPE,
    DAY_UTC,
)


class PrivatManager:

    def __init__(self, request):
        self.request = request

    balance_uri_body = '{0}?acc={1}&startDate={2}'
    statement_uri_body = '{0}?acc={1}&startDate={2}&limit={3}'

    currency_cashe_rate_uri = PRIVATBANK_CURRENCY_CASHE_RATE_URI
    currency_non_cashe_rate_uri = PRIVATBANK_CURRENCY_NON_CASHE_RATE_URI
    balance_uri = PRIVATBANK_BALANCE_URI
    statement_uri = PRIVATBANK_STATEMENT_URI
    payment_uri = PRIVATBANK_PAYMENT_URI

    document_number = DOCUMENT_NUMBER
    recipient_nceo = RECIPIENT_NCEO
    payment_naming = PAYMENT_NAMING
    recipient_ifi = RECIPIENT_IFI
    recipient_ifi_text = RECIPIENT_IFI_TEXT
    payment_destination = PAYMENT_DESTINATION
    payment_ccy = PAYMENT_CCY
    document_type = DOCUMENT_TYPE
    day_utc = DAY_UTC

    session = requests.Session()

    @staticmethod
    def __date(period: int) -> str:
        try:
            time_delta = int(datetime.now().timestamp()) - (period * DAY_UTC)
            dt_object = datetime.fromtimestamp(time_delta)
            year = dt_object.strftime("%Y")
            month = dt_object.strftime("%m")
            day = dt_object.strftime("%d")
            date = f"{day}-{str(month)}-{year}"
            return date
        except Exception as exc:
            exception = {
                "detail": str(exc)
            }
            return exception
    
    @classmethod
    def get_currency(
        cls,
        cashe_rate: bool
    ) -> Tuple[int, Dict[str, Any]]:
        try:
            if cashe_rate:
                uri = cls.currency_cashe_rate_uri
            else:
                uri = cls.currency_non_cashe_rate_uri
            response = cls.session.get(uri)
            response.raise_for_status()
            return response.status_code, response.json()
        except requests.exceptions.HTTPError as exc:
            error_response = {
                "detail": str(exc),
                "code": response.status_code,
            }
            return error_response
        except Exception as exc:
            exception = {
                "detail": str(exc)
            }
            return exception
    
    @classmethod
    def get_client_info(
            cls,
            token: str,
            iban: str
    ) -> Tuple[int, Dict[str, Any]]:
        try:
            date = cls.__date(0)
            uri = cls.balance_uri_body.format(
                cls.balance_uri, iban, date
            )
            headers = {"token": token}
            response = cls.session.get(uri, headers=headers)
            response.raise_for_status()
            return response.status_code, response.json()
        except requests.exceptions.HTTPError as exc:
            error_response = {
                "detail": str(exc),
                "code": response.status_code,
            }
            return error_response
        except Exception as exc:
            exception = {
                "detail": str(exc)
            }
            return exception

    @classmethod
    def get_privat_balance(
            cls,
            token: str,
            iban: str
    ) -> Tuple[int, Dict[str, Any]]:
        try:
            date = cls.__date(0)
            uri = cls.balance_uri_body.format(
                cls.balance_uri, iban, date
            )
            headers = {"token": token}
            response = cls.session.get(uri, headers=headers)
            response.raise_for_status()
            balance = {
                    "balance": response.json()["balances"][0]["balanceOutEq"]
                } 
            return response.status_code, balance
        except requests.exceptions.HTTPError as exc:
            error_response = {
                "detail": str(exc),
                "code": response.status_code,
            }
            return error_response
        except Exception as exc:
            exception = {
                "detail": str(exc)
            }
            return exception
        
    @classmethod
    def get_statement(
            cls,
            token: str,
            iban: str,
            period: int, # days
            limit: int
    ) -> Tuple[int, Dict[str, Any]]:
        try:
            date = cls.__date(period)
            uri = cls.statement_uri_body.format(
                cls.statement_uri, iban, date, limit
            )
            headers = {"token": token}
            response = cls.session.get(uri, headers=headers)
            response.raise_for_status()
            return response.status_code, response.json()
        except requests.exceptions.HTTPError as exc:
            error_response = {
                "detail": str(exc),
                "code": response.status_code,
            }
            return error_response
        except Exception as exc:
            exception = {
                "detail": str(exc)
            }
            return exception

    @classmethod
    def __payment_body(
        cls,
        recipient: str,
        amount: float,
        iban: str,
    ) -> Tuple[Dict[str, Any]]:
        try:
            body = {
                "document_number": cls.document_number,
                "recipient_card": recipient,
                "recipient_nceo": cls.recipient_nceo,
                "payment_naming": cls.payment_naming,
                "payment_amount": amount,
                "recipient_ifi": cls.recipient_ifi,
                "recipient_ifi_text": cls.recipient_ifi_text,
                "payment_destination": cls.payment_destination,
                "payer_account": iban,
                "payment_ccy": cls.payment_ccy,
                "document_type": cls.document_type
            }
            return body
        except Exception as exc:
            exception = {
                "detail": str(exc)
            }
            return exception
    
    @classmethod
    def create_payment(
        cls,
        token: str,
        iban: str,
        recipient: str,
        amount: float
    ) -> Tuple[int, Dict[str, Any]]:
        try:
            body = cls.__payment_body(recipient, amount, iban)
            data = json.dumps(body)
            headers = {"token": token}
            response = cls.session.post(
                cls.payment_uri, headers=headers, data=data
            )
            response.raise_for_status()
            return response.status_code, response.json()
        except requests.exceptions.HTTPError as exc:
            error_response = {
                "detail": str(exc),
                "code": response.status_code,
            }
            return error_response
        except Exception as exc:
            exception = {
                "detail": str(exc)
            }
            return exception
