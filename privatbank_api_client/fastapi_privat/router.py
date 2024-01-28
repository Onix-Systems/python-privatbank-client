from typing import Dict
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_privat.database import async_session
from fastapi_privat.schemas import (
    PrivatSchema,
    PrivatSchemaPayment,
    PrivatSchemaUpdate,
)
from async_privat.manager import AsyncPrivatManager
from fastapi_privat import crud


router = APIRouter(tags=["Privat"])


@router.post("/add-privat")
async def add_privatbank(
    schema: PrivatSchema, session: AsyncSession = Depends(async_session)
) -> Dict:
    try:
        response = await crud.create_privat(schema, session)
        return response
    except Exception as exc:
        exception = {"detail": str(exc)}
        return exception


@router.put("/change-privat")
async def change_privatbank(
    user_id: str,
    schema: PrivatSchemaUpdate,
    session: AsyncSession = Depends(async_session),
) -> Dict:
    try:
        response = await crud.update_privat(user_id, schema, session)
        return response
    except Exception as exc:
        exception = {"detail": str(exc)}
        return exception


@router.delete("/delete-privat")
async def delete_privatbank(
    user_id: str, session: AsyncSession = Depends(async_session)
) -> Dict:
    try:
        response = await crud.delete_privat(user_id, session)
        return response
    except Exception as exc:
        exception = {"detail": str(exc)}
        return exception


@router.get("/currencies")
async def currencies(cashe_rate: bool) -> Dict:
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
