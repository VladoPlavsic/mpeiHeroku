from fastapi import FastAPI, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every
import uvicorn

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

    # TODO This is cringe! Don't do this....
    def update():
        r = requests.put("http://localhost:1337/api/private/update/")

    @app.on_event("startup")
    @repeat_every(seconds=6 * 24 * 60 * 60) # update every 6 days
    def update_cdn_sharing_links() -> None:
        logger.warn("Updating sharing links invoked")
        update()


    app.include_router(api_router, prefix="/api")

    return app

app = get_application()
