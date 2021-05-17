from typing import Callable, Type
from databases import Database

from fastapi import Depends
from starlette.requests import Request

from app.db.repositories.base import BaseDBRepository

def get_database(requests: Request) -> Database:
    return requests.app.state._db

def get_db_repository(Repo_type: Type[BaseDBRepository]) -> Callable:
    def get_repo(db: Database = Depends(get_database)) -> Type[BaseDBRepository]:
        return Repo_type(db)
    
    return get_repo