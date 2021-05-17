import os
from fastapi import FastAPI
import boto3
from app.core.config import AWS_SECRET_KEY_ID, AWS_SECRET_ACCESS_KEY, CDN_ENDPOINT_URL 
import logging

logger = logging.getLogger(__name__)

async def connect_to_cdn(app: FastAPI) -> None:
    try:
        client = boto3.client(
            service_name='s3',
            endpoint_url=CDN_ENDPOINT_URL,
            aws_access_key_id=AWS_SECRET_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            aws_session_token=None,
            region_name=None,
            )

        app.state._cdn_client = client

    except Exception as e:
        logger.warn("--- s3 CONNECTION ERROR ---")
        logger.warn(e)
        logger.warn("--- s3 CONNECTION ERROR ---")