from fastapi import APIRouter

# private routes
from app.api.routes.private.post import router as private_post_router
from app.api.routes.private.get import router as private_get_router
from app.api.routes.private.put import router as private_put_router
from app.api.routes.private.delete import router as private_delete_router
# public routes
from app.api.routes.public.post import router as public_post_router
from app.api.routes.public.get import router as public_get_router
from app.api.routes.public.put import router as public_put_router
from app.api.routes.public.delete import router as public_delete_router
# user routes
from app.api.routes.users.post import router as users_post_router
from app.api.routes.users.get import router as users_get_router
from app.api.routes.users.put import router as users_put_router

# about routes
from app.api.routes.about.post import router as about_post_router
from app.api.routes.about.get import router as about_get_router
from app.api.routes.about.put import router as about_put_router
from app.api.routes.about.delete import router as about_delete_router

# news routes
from app.api.routes.news.post import router as news_post_router
from app.api.routes.news.get import router as news_get_router
from app.api.routes.news.put import router as news_put_router
from app.api.routes.news.delete import router as news_delete_router


router = APIRouter()

# private routes
router.include_router(private_post_router, prefix='/private', tags=["private"])
router.include_router(private_get_router, prefix='/private', tags=["private"])
router.include_router(private_put_router, prefix='/private', tags=["private"])
router.include_router(private_delete_router, prefix="/private", tags=["private"])

# public routes
router.include_router(public_post_router, prefix='/public', tags=["public"])
router.include_router(public_get_router, prefix='/public', tags=["public"])
router.include_router(public_put_router, prefix='/public', tags=["public"])
router.include_router(public_delete_router, prefix='/public', tags=["public"])

# users routes
router.include_router(users_post_router, prefix='/users', tags=['users'])
router.include_router(users_get_router, prefix='/users', tags=['users'])
router.include_router(users_put_router, prefix='/users', tags=['users'])


# about routes
router.include_router(about_post_router, prefix='/about', tags=['about'])
router.include_router(about_get_router, prefix='/about', tags=['about'])
router.include_router(about_put_router, prefix='/about', tags=['about'])
router.include_router(about_delete_router, prefix='/about', tags=['about'])

# news routes
router.include_router(news_post_router, prefix="/news", tags=['news'])
router.include_router(news_get_router, prefix="/news", tags=['news'])
router.include_router(news_put_router, prefix="/news", tags=['news'])
router.include_router(news_delete_router, prefix="/news", tags=['news'])
