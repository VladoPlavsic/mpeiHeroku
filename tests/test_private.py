import pytest

from httpx import AsyncClient

from fastapi import FastAPI

from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY, HTTP_200_OK, HTTP_409_CONFLICT

from typing import List

# ###
# import models
# ###

# request
from app.models.private import PresentationCreateModel

# response
from app.models.private import PresentationInDB

# ###
# decorate all tests with @pytest.mark.asyncio
# ###
pytestmark = pytest.mark.asyncio

def new_presentation():
    return PresentationCreateModel(
        name_ru='матрицы',
        description='Описание',
        fk=1,
        key='subscription/7-9/mathematics/algebra/matrix',
    )

class TestPrivatePostRoutes:

    @pytest.mark.parametrize("new_presentation, table", [(new_presentation(), 'theory'), (new_presentation(), 'practice')])
    async def test_post_create_not_existing_fk(self, app: FastAPI, client: AsyncClient, new_presentation: PresentationCreateModel, table: str) -> None:

        res = await client.post(app.url_path_for(f"private:post-{table}"), json=new_presentation.dict())
        assert res.status_code == HTTP_404_NOT_FOUND
        assert res.json()['detail'] == f"Insert {table} raised ForeignKeyViolationError. No such key in table lectures."



