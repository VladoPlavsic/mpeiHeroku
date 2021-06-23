from fastapi import FastAPI, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every

from app.api.routes import router as api_router
from app.core import config, tasks
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

    # Keep server alive
    @app.on_event("startup")
    @repeat_every(seconds=60 * 25) # update every 25 minutes (Keep server alive, remove on paid version)
    def keep_server_alive() -> None:
        logger.warn(f"sending GET request to {config.RESFUL_SERVER_URL}/api/public/wake/")
        requests.get(f"{config.RESFUL_SERVER_URL}/api/public/wake/")


    app.include_router(api_router, prefix="/api")

    return app

app = get_application()
