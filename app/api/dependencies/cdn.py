from typing import Callable, Type
import boto3

from fastapi import Depends
from starlette.requests import Request

from app.cdn.repositories.base import BaseCDNRepository

import logging
logger = logging.getLogger(__name__)


def get_cdn(requests: Request) -> boto3.client:
    return requests.app.state._cdn_client

def get_cdn_repository(Repo_type: Type[BaseCDNRepository]) -> Callable:
    def get_repo(cdn: boto3.client = Depends(get_cdn)) -> Type[BaseCDNRepository]:
        return Repo_type(cdn)

    return get_repo