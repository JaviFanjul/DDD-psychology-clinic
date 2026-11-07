from core.domain.unit_of_work import UnitOfWork, UnitOfWorkNotCommitted
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class PostgresUnitOfWork(UnitOfWork):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def commit(self) -> None:
        try:
            await self._session.commit()
        except SQLAlchemyError as error:
            raise UnitOfWorkNotCommitted() from error

    async def rollback(self) -> None:
        await self._session.rollback()
