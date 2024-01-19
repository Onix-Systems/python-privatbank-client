import json
import aiohttp
from typing import Dict
from privat_config.manager import BasePrivatManager


class AsyncPrivatManager(BasePrivatManager):
    @classmethod
    async def session(cls) -> aiohttp.client.ClientSession:
        return aiohttp.ClientSession()

    async def get_currencies(self, cashe_rate: bool) -> Dict:
        try:
            session = await self.session()
            if cashe_rate:
                uri = self.privat_currencies_cashe_rate_uri
            else:
                uri = self.privat_currencies_non_cashe_rate_uri
            async with session.get(uri) as response:
                try:
                    response = await session.get(uri)
                    code = response.status
                    response.raise_for_status()
                    detail = await response.json()
                    payload = {"code": code, "detail": detail}
                    return payload
                except aiohttp.ClientResponseError as exc:
                    error_response = {"code": code, "detail": str(exc.message)}
                    return error_response
        except Exception as exc:
            exception = {"detail": str(exc)}
            return exception

    async def get_client_info(self) -> Dict:
        try:
            session = await self.session()
            token = self.token
            iban = self.iban
            date = self.date(0).get("date")
            balance_uri = self.privat_balance_uri
            uri_body = self.privat_balance_uri_body
            uri = uri_body.format(balance_uri, iban, date)
            headers = {"token": token}
            async with session.get(uri, headers=headers) as response:
                try:
                    code = response.status
                    response.raise_for_status()
                    detail = await response.json()
                    payload = {"code": code, "detail": detail}
                    return payload
                except aiohttp.ClientResponseError as exc:
                    error_response = {"code": code, "detail": str(exc.message)}
                    return error_response
        except Exception as exc:
            exception = {"detail": str(exc)}
            return exception

    async def get_balance(self) -> Dict:
        try:
            client_info = await self.get_client_info()
            code = client_info.get("code")
            payload = client_info.get("detail")
            balance = {"code": code, "balance": payload["balances"][0]["balanceOutEq"]}
            return balance
        except Exception:
            return client_info

    async def get_statement(self, period: int, limit: int) -> Dict:
        try:
            session = await self.session()
            token = self.token
            iban = self.iban
            statement_uri = self.privat_statement_uri
            uri_body = self.privat_statement_uri_body
            date = self.date(period).get("date")
            uri = uri_body.format(statement_uri, iban, date, limit)
            headers = {"token": token}
            async with session.get(uri, headers=headers) as response:
                try:
                    code = response.status
                    response.raise_for_status()
                    detail = await response.json()
                    payload = {"code": code, "detail": detail}
                    return payload
                except aiohttp.ClientResponseError as exc:
                    error_response = {"code": code, "detail": str(exc.message)}
                    return error_response
        except Exception as exc:
            exception = {"detail": str(exc)}
            return exception

    async def create_payment(self, recipient: str, amount: float) -> Dict:
        try:
            session = await self.session()
            token = self.token
            iban = self.iban
            payment_body = self.payment_body(recipient, amount, iban)
            data = json.dumps(payment_body)
            headers = {"token": token}
            uri = self.privat_payment_uri
            async with session.post(uri, headers=headers, data=data) as response:
                try:
                    code = response.status
                    response.raise_for_status()
                    detail = await response.json()
                    payload = {"code": code, "detail": detail}
                    return payload
                except aiohttp.ClientResponseError as exc:
                    error_response = {"code": code, "detail": str(exc.message)}
                    return error_response
        except Exception as exc:
            exception = {"detail": str(exc)}
            return exception
