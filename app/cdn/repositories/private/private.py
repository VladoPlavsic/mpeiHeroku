from fastapi import HTTPException

from app.cdn.repositories.base import BaseCDNRepository
from app.cdn.types import DefaultFormats

import logging

logger = logging.getLogger(__name__)

class PrivateYandexCDNRepository(BaseCDNRepository):
    def get_background_url(self, *, object_key) -> str:
        """Generate presigned link for a single key. Returns presigned url"""
        suported_formats = DefaultFormats.IMAGES.formats
        if object_key.split('/')[-1].split('.')[-1] not in suported_formats:
            raise HTTPException(status_code=400, detail=f"Please specify key to file with one of the suported formats '{' ,'.join(suported_formats)}'")
        
        shared = self._BaseCDNRepository__get_presigned_links_from_list_of_keys(list_of_keys=[object_key])

        if not shared:
            raise HTTPException(status_code=404, detail=f"Sharing background image returned None. Tried to share {object_key}")

        return shared[0][object_key]