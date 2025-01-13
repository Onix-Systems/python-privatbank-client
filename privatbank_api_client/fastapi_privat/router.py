from typing import Dict
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from privatbank_api_client.fastapi_privat.database import async_session
from privatbank_api_client.fastapi_privat.schemas import (
    PrivatSchema,
    PrivatSchemaPayment,
    PrivatSchemaUpdate,
)
from privatbank_api_client.async_privat.manager import AsyncPrivatManager
from privatbank_api_client.fastapi_privat import crud

"""
This module provides a FastAPI APIRouter implementation for managing 
PrivatBank-related operations, such as creating users, updating records,
fetching account details, balances, payment transactions, etc. 
Each route handles a specific request, interacts with relevant database
managers (CRUD or external API manager), and ensures error handling
for unfulfilled requests or internal issues.

Routes and their functionalities:
- `/add`: Add a new PrivatBank user record.
- `/change`: Edit the record of a specific PrivatBank user.
- `/delete`: Remove a user from the PrivatBank records.
- `/currencies`: Fetch current currency exchange rates.
- `/client_info`: Retrieve client-specific details from PrivatBank.
- `/balance`: Fetch the user's bank account balance.
- `/statement`: Get a transaction statement for the specified time period.
- `/payment`: Perform a payment to another account.
"""

router = APIRouter(tags=["Privat"], prefix="/privat")


@router.post("/add")
async def add_privatbank(
    schema: PrivatSchema, session: AsyncSession = Depends(async_session)
) -> Dict:
    """
    Add a new PrivatBank user record to the database.

    :param schema: PrivatSchema object containing user details.
    :param session: Database session dependency for async queries.
    :return: Dictionary with the creation response or error details.
    :raises: Exception in case of database or internal issues.
    """
    try:
        response = await crud.create_privat(schema, session)
        return response
    except Exception as exc:
        exception = {"detail": str(exc)}
        return exception


@router.put("/change")
async def change_privatbank(
    user_id: str,
    schema: PrivatSchemaUpdate,
    session: AsyncSession = Depends(async_session),
) -> Dict:
    """
    Update an existing PrivatBank user record.

    :param user_id: Unique identifier of the user to be updated.
    :param schema: PrivatSchemaUpdate object with updated details.
    :param session: Database session dependency for async queries.
    :return: Dictionary with the update response or error details.
    :raises: Exception in case of database or internal issues.
    """
    try:
        response = await crud.update_privat(user_id, schema, session)
        return response
    except Exception as exc:
        exception = {"detail": str(exc)}
        return exception


@router.delete("/delete")
async def delete_privatbank(
    user_id: str, session: AsyncSession = Depends(async_session)
) -> Dict:
    """
    Delete a PrivatBank user record from the database.

    :param user_id: Unique identifier of the user to delete.
    :param session: Database session dependency for async queries.
    :return: Dictionary with the deletion response or error details.
    :raises: Exception in case of database or internal issues.
    """
    try:
        response = await crud.delete_privat(user_id, session)
        return response
    except Exception as exc:
        exception = {"detail": str(exc)}
        return exception


@router.get("/currencies")
async def currencies(cashe_rate: bool) -> Dict:
    """
    Fetch current currency exchange rates from PrivatBank.

    :param cashe_rate: Boolean indicating if cash rates should be fetched.
    :return: Dictionary with current exchange rates or error details.
    :raises: Exception in case of an internal issue or API failure.
    """
    try:
        mng = AsyncPrivatManager()
        response = await mng.get_currencies(cashe_rate)
        return response
    except Exception as exc:
        exception = {"detail": str(exc)}
        return exception


@router.get("/client_info")
async def client_info(
    user_id: str, session: AsyncSession = Depends(async_session)
) -> Dict:
    """
    Retrieve client-specific details from PrivatBank.

    :param user_id: Unique identifier of the user.
    :param session: Database session dependency for async queries.
    :return: Dictionary with client details or error information.
    :raises: Exception in case of internal issues or missing user records.
    """
    try:
        mng = AsyncPrivatManager()
        payload = await crud.read_privat(user_id, session)
        if payload is not None:
            mng.token = payload[0].privat_token
            mng.iban = payload[0].privat_iban
            response = await mng.get_client_info()
        else:
            response = mng.does_not_exsists_exception()
        return response
    except Exception as exc:
        exception = {"detail": str(exc)}
        return exception


@router.get("/balance")
async def balance(user_id: str, session: AsyncSession = Depends(async_session)) -> Dict:
    """
    Fetch the account balance for a given PrivatBank user.

    :param user_id: Unique identifier of the user.
    :param session: Database session dependency for async queries.
    :return: Dictionary with account balance or error details.
    :raises: Exception in case of internal issues or API failure.
    """
    try:
        mng = AsyncPrivatManager()
        payload = await crud.read_privat(user_id, session)
        if payload is not None:
            mng.token = payload[0].privat_token
            mng.iban = payload[0].privat_iban
            response = await mng.get_balance()
        else:
            response = mng.does_not_exsists_exception()
        return response
    except Exception as exc:
        exception = {"detail": str(exc)}
        return exception


@router.get("/statement")
async def statement(
    user_id: str,
    period: int,
    limit: int,
    session: AsyncSession = Depends(async_session),
) -> Dict:
    """
    Retrieve a transaction statement for the specified user.

    :param user_id: Unique identifier of the user.
    :param period: Time period (in days) for the statement.
    :param limit: Maximum number of transaction records to fetch.
    :param session: Database session dependency for async queries.
    :return: Dictionary with transaction details or error information.
    :raises: Exception in case of internal issues or API failure.
    """
    try:
        mng = AsyncPrivatManager()
        payload = await crud.read_privat(user_id, session)
        if payload is not None:
            mng.token = payload[0].privat_token
            mng.iban = payload[0].privat_iban
            response = await mng.get_statement(period, limit)
        else:
            response = mng.does_not_exsists_exception()
        return response
    except Exception as exc:
        exception = {"detail": str(exc)}
        return exception


@router.post("/payment")
async def payment(
    schema: PrivatSchemaPayment, session: AsyncSession = Depends(async_session)
) -> Dict:
    """
    Perform a payment to another account using PrivatBank.

    :param schema: PrivatSchemaPayment object with recipient and amount details.
    :param session: Database session dependency for async queries.
    :return: Dictionary with payment confirmation or error details.
    :raises: Exception in case of internal issues or API failure.
    """
    try:
        mng = AsyncPrivatManager()
        payload = await crud.read_privat(schema.user_id, session)
        if payload is not None:
            mng.token = payload[0].privat_token
            mng.iban = payload[0].privat_iban
            response = await mng.create_payment(schema.recipient, schema.amount)
        else:
            response = mng.does_not_exsists_exception()
        return response
    except Exception as exc:
        exception = {"detail": str(exc)}
        return exception
