from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every

from starlette.requests import Request
from starlette.responses import Response

from app.api.routes import router as api_router
from app.core import config, tasks
from app.api.dependencies.email import send_message
import requests

import logging

logger = logging.getLogger(__name__)

def get_application():
    
    app = FastAPI(title=config.PROJECT_NAME, version=config.VERSION)
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    # Send email on server error
    async def catch_exceptions_middleware(request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            send_message(subject="Server error", message_text=f"Error on server occured. {e}")
            logger.error("----- 500 INTERNAL SERVER ERROR -----")
            logger.error(e)
            logger.error("----- 500 INTERNAL SERVER ERROR -----")
            return Response("Internal server error", status_code=500)
    
    # Add middleware for sending error email
    app.middleware('http')(catch_exceptions_middleware)

    app.add_event_handler("startup", tasks.create_start_app_handler(app))
    app.add_event_handler("shutdown", tasks.create_stop_app_handler(app))

    # weekly sharing link update
    @app.on_event("startup")
    @repeat_every(seconds=6 * 24 * 60 * 60) # update every 6 days
    def update_cdn_sharing_links() -> None:
        logger.warn(f"sending PUT request to {config.RESFUL_SERVER_URL}/api/public/update/")
        requests.put(f"{config.RESFUL_SERVER_URL}/api/private/update/")

    # Daily check for expired subscriptions
    @app.on_event("startup")
    @repeat_every(seconds=24 * 60 * 60)
    def expired_subscriptions_check():
        logger.warn(f"sending POST request to {config.RESFUL_SERVER_URL}/api/users/subscriptions/check/")
        requests.post(f"{config.RESFUL_SERVER_URL}/api/users/subscriptions/check/")

    # Daily check for deactivated profiles
    @app.on_event("startup")
    @repeat_every(seconds=24 * 60 * 60)
    def deactivated_profiles_check():
        logger.warn(f"sending POST request to {config.RESFUL_SERVER_URL}/api/users/deactivated/check/")
        requests.post(f"{config.RESFUL_SERVER_URL}/api/users/deactivated/check/")

    # Keep server alive
    @app.on_event("startup")
    @repeat_every(seconds=60 * 25) # update every 25 minutes (Keep server alive, remove on paid version)
    def keep_server_alive() -> None:
        logger.warn(f"sending GET request to {config.RESFUL_SERVER_URL}/api/public/wake/")
        requests.get(f"{config.RESFUL_SERVER_URL}/api/public/wake/")


    app.include_router(api_router, prefix="/api")

    return app

app = get_application()
