from fastapi import APIRouter
from fastapi import Depends, Body
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

from app.api.dependencies.cdn import get_cdn_repository
from app.cdn.repositories.news.news import NewsYandexCDNRepository

from app.api.dependencies.database import get_db_repository
from app.db.repositories.news.news import NewsDBRepository

from app.api.dependencies.auth import allowed_or_denied

# request models
from app.models.news import NewsPostModel
from app.models.news import NewsCreateModel

# response models
from app.models.news import NewsInDBModel
from app.models.core import AllowCreate

from app.cdn.types import DefaultFormats

router = APIRouter()

@router.post("/check", response_model=AllowCreate, name="news:check-create", status_code=HTTP_200_OK)
async def check_create_news(
    date: str,
    url: str,
    db_repo: NewsYandexCDNRepository = Depends(get_db_repository(NewsDBRepository))
    ) -> AllowCreate:
    """Try creating practice. If OK is returned {OK: True}, practice can be created, else there is something wrong with it."""
    response = await db_repo.insert_news_check(date=date, url=url)
    
    return AllowCreate(OK=response)

@router.post("/create", response_model=NewsInDBModel, name="news:create", status_code=HTTP_201_CREATED)
async def create_news(
    news: NewsPostModel = Body(...),
    db_repo: NewsDBRepository = Depends(get_db_repository(NewsDBRepository)),
    cdn_repo: NewsYandexCDNRepository = Depends(get_cdn_repository(NewsYandexCDNRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> NewsInDBModel:

    preview_image_url = cdn_repo.get_sharing_link_from_object_key(object_key=news.object_key)
    images = cdn_repo.format_presentation_content(folder=news.folder, type_=DefaultFormats.IMAGES)

    create_news_model = NewsCreateModel(**news.dict(), preview_image_url=preview_image_url[news.object_key], images=images)
    response = await db_repo.insert_news(news=create_news_model)

    return response
