import requests
import json
from datetime import datetime
from typing import Tuple, Dict

from .config import (
    PRIVATBANK_CURRENCY_CASHE_RATE_URI,
    PRIVATBANK_CURRENCY_NON_CASHE_RATE_URI,
    PRIVATBANK_BALANCE_URI,
    PRIVATBANK_BALANCE_URI_BODY,
    PRIVATBANK_STATEMENT_URI,
    PRIVATBANK_STATEMENT_URI_BODY,
    PRIVATBANK_PAYMENT_URI,

    DOCUMENT_NUMBER,
    DOCUMENT_TYPE,
    PAYMENT_CCY,
    PAYMENT_DESTINATION,
    PAYMENT_NAMING,
    RECIPIENT_IFI,
    RECIPIENT_IFI_TEXT,
    RECIPIENT_NCEO,
)

class PrivatManager:

    def __init__(self, request, token=None, iban=None):
        self.request = request
        self._token = token
        self._iban = iban

    _session = requests.Session()

    _privat_balance_uri_body = PRIVATBANK_BALANCE_URI_BODY
    _privat_statement_uri_body = PRIVATBANK_STATEMENT_URI_BODY

    _privat_currency_cashe_rate_uri = PRIVATBANK_CURRENCY_CASHE_RATE_URI
    _privat_currency_non_cashe_rate_uri = PRIVATBANK_CURRENCY_NON_CASHE_RATE_URI
    _privat_balance_uri = PRIVATBANK_BALANCE_URI
    _privat_statement_uri = PRIVATBANK_STATEMENT_URI
    _privat_payment_uri = PRIVATBANK_PAYMENT_URI

    _document_number = DOCUMENT_NUMBER
    _document_type = DOCUMENT_TYPE
    _payment_ccy = PAYMENT_CCY
    _payment_destination = PAYMENT_DESTINATION
    _payment_naming = PAYMENT_NAMING
    _recipient_ify = RECIPIENT_IFI
    _recipient_ify_text = RECIPIENT_IFI_TEXT
    _recipient_nceo = RECIPIENT_NCEO

    _day_unix = 86400

    @property
    def token(self):
        return self._token
    
    @token.setter
    def token(self, new_token):
        self._token = new_token

    @property
    def iban(self):
        return self._iban
    
    @iban.setter
    def iban(self, new_iban):
        self._iban = new_iban

    @property
    def privat_currency_cashe_rate_uri(self):
        return self._privat_currency_cashe_rate_uri
    
    @privat_currency_cashe_rate_uri.setter
    def privat_currency_cashe_rate_uri(self, new_uri):
        self._privat_currency_cashe_rate_uri = new_uri
    
    @property
    def privat_currency_non_cashe_rate_uri(self):
        return self._privat_currency_non_cashe_rate_uri
    
    @privat_currency_non_cashe_rate_uri.setter
    def privat_currency_non_cashe_rate_uri(self, new_uri):
        self._privat_currency_non_cashe_rate_uri = new_uri

    @property
    def privat_balance_uri(self):
        return self._privat_balance_uri
    
    @privat_balance_uri.setter
    def privat_balance_uri(self, new_uri):
        self._privat_balance_uri = new_uri

    @property
    def privat_statement_uri(self):
        return self._privat_statement_uri
    
    @privat_statement_uri.setter
    def privat_statement_uri(self, new_uri):
        self._privat_statement_uri = new_uri

    @property
    def privat_payment_uri(self):
        return self._privat_payment_uri

    @privat_payment_uri.setter
    def privat_payment_uri(self, new_uri):
        self._privat_payment_uri = new_uri

    @property
    def privat_balance_uri_body(self):
        return self._privat_balance_uri_body

    @privat_balance_uri_body.setter
    def privat_balance_uri_body(self, new_uri_body):
        self._privat_balance_uri_body = new_uri_body

    @property
    def privat_statement_uri_body(self):
        return self._privat_statement_uri_body
    
    @privat_statement_uri_body.setter
    def privat_statement_uri_body(self, new_uri_body):
        self._privat_statement_uri_body = new_uri_body
    
    @property
    def document_number(self):
        return self._document_number
    
    @document_number.setter
    def document_number(self, new_document_number):
        self._document_number = new_document_number

    @property
    def document_type(self):
        return self._document_type
    
    @document_type.setter
    def document_type(self, new_document_type):
        self._document_type = new_document_type

    @property
    def payment_ccy(self):
        return self._payment_ccy
    
    @payment_ccy.setter
    def payment_ccy(self, new_payment_ccy):
        self._payment_ccy = new_payment_ccy

    @property
    def payment_destination(self):
        return self._payment_destination
    
    @payment_destination.setter
    def payment_destination(self, new_payment_destination):
        self._payment_destination = new_payment_destination
    
    @property
    def payment_naming(self):
        return self._payment_naming
    
    @payment_naming.setter
    def payment_naming(self, new_payment_naming):
        self._payment_naming = new_payment_naming

    @property
    def recipient_ify(self):
        return self._recipient_ify
    
    @recipient_ify.setter
    def recipient_ify(self, new_recipient_ify):
        self._recipient_ify = new_recipient_ify

    @property
    def recipient_ify_text(self):
        return self._recipient_ify_text
    
    @recipient_ify_text.setter
    def recipient_ify_text(self, new_recipient_ify_text):
        self._recipient_ify_text = new_recipient_ify_text

    @property
    def recipient_nceo(self):
        return self._recipient_nceo
    
    @recipient_nceo.setter
    def recipient_nceo(self, new_recipient_nceo):
        self._recipient_nceo = new_recipient_nceo

    def get_currency(self, cashe_rate: bool) -> Tuple[int, Dict]:
        try:
            session = self._session
            if cashe_rate:
                uri = self._privat_currency_cashe_rate_uri
            else:
                uri = self._privat_currency_non_cashe_rate_uri
            response = session.get(uri)
            return response.status_code, response.json()  
        except requests.exceptions.HTTPError as exc:
            error_response = {
                "code": response.status_code,
                "detail": str(exc)
            }
            return error_response
        except Exception as exc:
            exception = {
                "detail": str(exc)
            }
            return exception                 

    def get_client_info(self) -> Tuple[int, Dict]:
        try:
            session = self._session
            token = self._token
            iban = self._iban
            date = self.__date(0)
            balance_uri = self._privat_balance_uri
            uri_body = self._privat_balance_uri_body
            uri = uri_body.format(balance_uri, iban, date)
            headers = {"token": token}
            response = session.get(uri, headers=headers)
            return response.status_code, response.json()
        except requests.exceptions.HTTPError as exc:
            error_response = {
                "code": response.status_code,
                "detail": str(exc)
            }
            return error_response
        except Exception as exc:
            exception = {
                "detail": str(exc)
            }
            return exception

    def get_balance(self) -> Tuple[int, Dict]:
        try:
            response = self.get_client_info()
            code = response[0]
            payload = response[1]
            balance = {
                "balance": payload["balances"][0]["balanceOutEq"]
            }
            return code, balance
        except Exception:
            return response

    def get_statement(self, period: int, limit: int) -> Tuple[int, Dict]:
        try:
            session = self._session
            token = self._token
            iban = self._iban
            date = self.__date(period)
            statement_uri = self._privat_statement_uri
            uri_body = self._privat_statement_uri_body
            uri = uri_body.format(statement_uri, iban, date, limit)
            headers = {"token": token}
            response = session.get(uri, headers=headers)
            return response.status_code, response.json()
        except requests.exceptions.HTTPError as exc:
            error_response = {
                "code": response.status_code,
                "detail": str(exc)
            }
            return error_response
        except Exception as exc:
            exception = {
                "detail": str(exc)
            }
            return exception
        
    def create_payment(self, recipient: str, amount: float) -> Tuple[int, Dict]:
        try:
            session = self._session
            token = self._token
            iban = self._iban
            payment_body = self.__payment_body(recipient, amount, iban)
            data = json.dumps(payment_body)
            headers = {"token": token}
            uri = self._privat_payment_uri
            response = session.post(uri, headers=headers, data=data)
            return response.status_code, response.json()
        except requests.exceptions.HTTPError as exc:
            error_response = {
                "code": response.status_code,
                "detail": str(exc)
            }
            return error_response
        except Exception as exc:
            exception = {
                "detail": str(exc)
            }
            return exception
        
    def __date(self, period: int) -> str:
        try:
            time_delta = int(datetime.now().timestamp()) - (period * self._day_unix)
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

    def __payment_body(self, recipient: str, amount: float, iban: str) -> Tuple[Dict]:
        try:
            payment_body = {
                "document_number": self._document_number,
                "recipient_card": recipient,
                "recipient_nceo": self._recipient_nceo,
                "payment_naming": self._payment_naming,
                "payment_amount": amount,
                "recipient_ifi": self._recipient_ify,
                "recipient_ifi_text": self._recipient_ify_text,
                "payment_destination": self._payment_destination,
                "payer_account": iban,
                "payment_ccy": self._payment_ccy,
                "document_type": self._document_type
            }
            return payment_body
        except Exception as exc:
            exception = {
                "detail": str(exc)
            }
            return exception
