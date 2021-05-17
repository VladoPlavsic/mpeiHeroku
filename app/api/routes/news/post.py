from fastapi import APIRouter, HTTPException
from fastapi import Depends, Body
from starlette.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN

from app.api.dependencies.cdn import get_cdn_repository
from app.cdn.repositories.news.news import NewsYandexCDNRepository

from app.api.dependencies.database import get_db_repository
from app.db.repositories.news.news import NewsDBRepository

from app.api.dependencies.auth import is_superuser, is_verified

# request models
from app.models.news import NewsPostModel
from app.models.news import NewsCreateModel

# response models
from app.models.news import NewsInDBModel

router = APIRouter()

@router.post("/create", response_model=NewsInDBModel, name="news:create", status_code=HTTP_201_CREATED)
async def create_news(
    news: NewsPostModel = Body(...),
    db_repo: NewsDBRepository = Depends(get_db_repository(NewsDBRepository)),
    cdn_repo: NewsYandexCDNRepository = Depends(get_cdn_repository(NewsYandexCDNRepository)),
    is_superuser = Depends(is_superuser),
    is_verified = Depends(is_verified),
    ) -> NewsInDBModel:

    if not is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    if not is_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")
        

    # get images formed data    
    preview_image_url = cdn_repo.get_sharing_links_from_keys(list_of_objects=[{"Key": news.cloud_key}])
    images = cdn_repo.form_images_insert_data(prefix=news.folder, image_prefix="images")

    create_model = NewsCreateModel(
        cloud_key=news.cloud_key,
        content=news.content,
        date=news.date,
        short_desc=news.short_desc,
        title=news.title,
        url=news.url,
        preview_image_url=preview_image_url[news.cloud_key], 
        images=images)    

    # insert into database
    response = await db_repo.insert_news(news=create_model)

    return response