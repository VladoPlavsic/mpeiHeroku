from typing import List
from fastapi import APIRouter
from fastapi import Depends
from starlette.status import HTTP_200_OK

from app.api.dependencies.database import get_db_repository
from app.db.repositories.news.news import NewsDBRepository

# response models
from app.models.news import NewsInDBModel, NewsResponseModel
from app.models.news import NewsPreviewInDBModel

router = APIRouter()

@router.get("/get/count")
async def get_news_count(
    db_repo: NewsDBRepository = Depends(get_db_repository(NewsDBRepository)),
    ) -> int:

    return await db_repo.get_news_count()

@router.get("/get/news/preview", response_model=NewsResponseModel, name="news:get-news", status_code=HTTP_200_OK)
async def get_news_preview(
    start: int,
    count: int,
    db_repo: NewsDBRepository = Depends(get_db_repository(NewsDBRepository)),
    ) -> NewsResponseModel:

    news = await db_repo.select_news_preview(start=start, count=count)
    count = await db_repo.get_news_count()

    return NewsResponseModel(news=news, count=count)

@router.get("/get/news", response_model=NewsInDBModel, name="news:get-news", status_code=HTTP_200_OK)
async def get_news(
    date: str,
    url: str,
    db_repo: NewsDBRepository = Depends(get_db_repository(NewsDBRepository)),
    ) -> NewsInDBModel:

    news = await db_repo.select_news(date=date, url=url)

    return news