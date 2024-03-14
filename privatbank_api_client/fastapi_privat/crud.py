from typing import Dict
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_privat.models import PrivatModel as mdl
from fastapi_privat.schemas import PrivatSchema, PrivatSchemaUpdate
from async_privat.manager import AsyncPrivatManager


async def create_privat(schema: PrivatSchema, session: AsyncSession) -> Dict:
    try:
        mng = AsyncPrivatManager()
        query = await session.execute(select(mdl).where(mdl.user_id == schema.user_id))
        if query.first() is not None:
            return mng.exists_exception()
        new_obj = insert(mdl).values(**schema.model_dump())
        await session.execute(new_obj)
        await session.commit()
        return mng.create_success()
    except Exception as exc:
        exception = {"detail": str(exc)}
        return exception


async def read_privat(user_id: str, session: AsyncSession) -> Dict:
    try:
        query = await session.execute(select(mdl).where(mdl.user_id == user_id))
        return query.first()
    except Exception as exc:
        exception = {"detail": str(exc)}
        return exception


async def update_privat(
    user: str, schema: PrivatSchemaUpdate, session: AsyncSession
) -> Dict:
    try:
        mng = AsyncPrivatManager()
        query = await session.execute(select(mdl).where(mdl.user_id == user))
        if query.first() is not None:
            query = await session.execute(
                update(mdl).values(**schema.model_dump()).where(mdl.user_id == user)
            )
            await session.commit()
            return mng.update_success()
        return mng.does_not_exsists_exception()
    except Exception as exc:
        exception = {"detail": str(exc)}
        return exception


async def delete_privat(user: str, session: AsyncSession) -> Dict:
    try:
        mng = AsyncPrivatManager()
        query = await session.execute(select(mdl).where(mdl.user_id == user))
        if query.first() is not None:
            query = await session.execute(delete(mdl).where(mdl.user_id == user))
            await session.commit()
            return mng.delete_success()
        return mng.does_not_exsists_exception()
    except Exception as exc:
        exception = {"detail": str(exc)}
        return exception
