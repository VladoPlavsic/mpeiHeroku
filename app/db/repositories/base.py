from databases import Database
from fastapi import HTTPException

from databases.backends.postgres import Record
from app.db.repositories.types import QueryReturnType

import logging

logger = logging.getLogger(__name__)

class BaseDBRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    async def __execute(self, *, query: str, type_: QueryReturnType):
        """This function executes query based on needed return type.
        
        This function has multiple return types:
        1. None
        2. Record
        3. List[Record]
        4. Single column value
        """
        try:
            if type_ == QueryReturnType.EXECUTE_ONE:
                await self.db.execute(query=query)
            elif type_ == QueryReturnType.EXECUTE_MANY:
                await self.db.execute_many(query=query)
            elif type_ == QueryReturnType.FETCH_ONE:
                return await self.db.fetch_one(query=query)
            elif type_ == QueryReturnType.FETCH_MANY:
                return await self.db.fetch_all(query=query)
            elif type_ == QueryReturnType.FETCH_ONE_VAL:
                return await self.db.fetch_val(query=query)
            else:
                raise Exception("Tried to use unknow Enum.")
        except Exception as e:
            logger.error("---DATABASE QUERY ERROR---")
            logger.error(f"{e}")
            logger.error("---DATABASE QUERY ERROR---")
            raise HTTPException(status_code=400, detail=f"Database exception. Exited with {e}")

    async def _execute_one(self, *, query: str) -> None:
        """This function tries to execute query. Doesn't return anything"""
        await self.__execute(query=query, type_=QueryReturnType.EXECUTE_ONE)

    async def _execute_many(self, *, query: str) -> None:
        """This function tries to execute query. Doesn't return anything."""
        await self.__execute(query=query, type_=QueryReturnType.EXECUTE_MANY)

    async def _fetch_one(self, *, query: str) -> Record:
        """This function tries to execute query. Returns one record from db."""
        return await self.__execute(query=query, type_=QueryReturnType.FETCH_ONE)

    async def _fetch_many(self, *, query: str) -> Record:
        """This function tries to execute query. Returns many records from db."""
        return await self.__execute(query=query, type_=QueryReturnType.FETCH_MANY)

    async def _fetch_value(self, *, query: str):
        """This function tries to execute query. Returns single value from db."""
        return await self.__execute(query=query, type_=QueryReturnType.FETCH_ONE_VAL)
