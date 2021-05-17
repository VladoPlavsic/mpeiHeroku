from fastapi import HTTPException

from app.cdn.repositories.base import BaseCDNRepository

from app.models.public import PresentationMediaCreate
from app.cdn.repositories.parsers import *

class PublicYandexCDNRepository(BaseCDNRepository):
    def form_presentation_insert_data(self, *, prefix, image_prefix="img", audio_prefix="mp3") -> Tuple:
        '''
        Accepts prefix, image_prefix, audio_prefix

            prefix - key to folder containing audio and image folders
            image_prefix - image folder name
            audio_prefix - audio folder name

        Returns 
            Tuple of formed data for inserting
            images = List[PresentationMediaCreate]
            audio = List[PresentationMediaCreate]
        '''
        # get all keys for a given prefix
        prefix = prefix if prefix[-1] == '/' else prefix + '/'
        self.get_object_keys(prefix=prefix)

        image_prefix = prefix + image_prefix
        audio_prefix = prefix + audio_prefix

        # in case we got two '/' 
        image_prefix = image_prefix.replace('//', '/')
        audio_prefix = audio_prefix.replace('//', '/')

        image_key_order = self.get_key_order_pairs(prefix=image_prefix)
        audio_key_order = self.get_key_order_pairs(prefix=audio_prefix)

        image = self.get_sharing_links_from_keys(prefix=image_prefix)
        audio = self.get_sharing_links_from_keys(prefix=audio_prefix)

        images = []
        for key, value in image.items():
            try:
                images.append(PresentationMediaCreate(order=image_key_order[key], url=value, key=key))
            except:
                pass

        audios = []
        for key, value in audio.items():
            try:
                audios.append(PresentationMediaCreate(order=audio_key_order[key], url=value, key=key))
            except:
                pass

        if not images:
            raise HTTPException(status_code=404, detail=f"No images found a path {prefix}. Images must be present!")

        return (images, audios)