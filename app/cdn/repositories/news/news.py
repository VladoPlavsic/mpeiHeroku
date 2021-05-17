from typing import List
from fastapi import HTTPException

from app.cdn.repositories.base import BaseCDNRepository

from app.models.news import NewsImagesCreate


class NewsYandexCDNRepository(BaseCDNRepository):
    def form_images_insert_data(self, *, prefix, image_prefix="img") -> List:
        '''
        Accepts prefix, image_prefix

            prefix - key to folder containing image folders
            image_prefix - image folder name

        Returns 
            List of formed data for inserting
            images = List[NewsImagesCreate]
        '''
        # get all keys for a given prefix
        prefix = prefix if prefix[-1] == '/' else prefix + '/'
        self.get_object_keys(prefix=prefix)

        image_prefix = prefix + image_prefix

        # in case we got two '/' 
        image_prefix = image_prefix.replace('//', '/')

        image_key_order = self.get_key_order_pairs(prefix=image_prefix)

        image = self.get_sharing_links_from_keys(prefix=image_prefix)

        images = []
        for key, value in image.items():
            try:
                images.append(NewsImagesCreate(order=image_key_order[key], url=value, cloud_key=key))
            except:
                pass

        if not images:
            raise HTTPException(status_code=404, detail=f"No images found a path {prefix}. Images must be present!")

        return images