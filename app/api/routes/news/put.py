from fastapi import APIRouter, HTTPException
from fastapi import Depends, Body
from starlette.status import HTTP_200_OK, HTTP_403_FORBIDDEN

from app.api.dependencies.cdn import get_cdn_repository
from app.cdn.repositories.news.news import NewsYandexCDNRepository

from app.api.dependencies.database import get_db_repository
from app.db.repositories.news.news import NewsDBRepository

from app.api.dependencies.auth import is_superuser, is_verified

# request models
from app.models.news import NewsUpdateModel

# response models
from app.models.news import NewsInDBModel

router = APIRouter()

@router.put("/update", response_model=NewsInDBModel, name="news:uodate", status_code=HTTP_200_OK)
async def create_news(
    updated: NewsUpdateModel = Body(...),
    db_repo: NewsDBRepository = Depends(get_db_repository(NewsDBRepository)),
    cdn_repo: NewsYandexCDNRepository = Depends(get_cdn_repository(NewsYandexCDNRepository)),
    is_superuser = Depends(is_superuser),
    is_verified = Depends(is_verified),
    ) -> NewsInDBModel:

    if not is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    if not is_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")
        

    # get preview image link if cloud_key
    preview_image_url = \
         cdn_repo.get_sharing_links_from_keys(list_of_objects=[{"Key": updated.cloud_key}]) \
             if updated.cloud_key else None

    updated.preview_image_url = preview_image_url[updated.cloud_key] if preview_image_url else None

    return await db_repo.update_news_metadata(updated=updated)