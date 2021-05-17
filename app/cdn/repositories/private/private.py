from typing import Dict, List, Tuple, Union
from app.cdn.repositories.base import BaseCDNRepository
from app.core.config import BUCKET, CDN_LINK_LIFESPAN

# exceptions
from fastapi import HTTPException

from app.models.private import PresentationMediaCreate

from app.models.private import StructureAllModel
from app.models.private import MaterialAllModel
from app.models.private import AudioImagesAllModel

# parsers
from app.cdn.repositories.parsers import *

import logging

logger = logging.getLogger(__name__)

class PrivateYandexCDNRepository(BaseCDNRepository):
    def form_presentation_insert_data(self, *, prefix, fk, image_prefix="img", audio_prefix="mp3") -> Tuple:
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
                images.append(PresentationMediaCreate(order=image_key_order[key], url=value, fk=fk, key=key))
            except:
                pass

        audios = []
        for key, value in audio.items():
            try:
                audios.append(PresentationMediaCreate(order=audio_key_order[key], url=value, fk=fk, key=key))
            except:
                pass

        if not images:
            raise HTTPException(status_code=404, detail=f"No images found a path {prefix}. Images must be present!")

        return (images, audios)


    def get_background_url(self, *, key, remove_extra=False) -> str:
        '''
        Accepts key to object of type (suported_formats)

        remove_extra: False | True -> If set to true, this will remove all files from a folder
        that do not equal to key parameter. NOTE: If u set remove_extra to True and you indicate wrong key
        this will remove the wanted key from folder
        '''
        suported_formats = ['jpg']
        if key.split('/')[-1].split('.')[-1] not in suported_formats:
            raise HTTPException(status_code=400, detail=f"Please specify key to file with one of the suported formats '{' ,'.join(suported_formats)}'")

        folder_prefix = key.replace(key.split('/')[-1], '')

        if remove_extra: 
            content_list = self.get_object_keys(prefix=key.split('/')[0], update=True)
            to_be_removed = list_root_directory_files(prefix=folder_prefix, content_list=content_list, exclude_files=[key])
            self.delete_keys(list_of_keys=to_be_removed)        

        link = self.get_sharing_links_from_keys(list_of_objects=[{"Key": key}], check_key=True)

        try:
            return link[key]
        except KeyError:
            raise HTTPException(status_code=404, detail="Background key error. Check your post data, and cdn! We didn't find any data in cdn for a given key")


    def create_key_list_from_lists_of_objects(
        self, 
        *,
        grades: List[StructureAllModel],
        subjects: List[StructureAllModel],
        branches: List[StructureAllModel],
        lectures: List[StructureAllModel],
        books: List[MaterialAllModel],
        theory_images: List[AudioImagesAllModel],
        theory_audio: List[AudioImagesAllModel],
        practice_images: List[AudioImagesAllModel],
        practice_audio: List[AudioImagesAllModel],
        ) -> None:

        keys = {}
        keys["grades"] = structure_keys_from_list_of_objects(grades)
        keys["subjects"] = structure_keys_from_list_of_objects(subjects)
        keys["branches"] = structure_keys_from_list_of_objects(branches)
        keys["lectures"] = structure_keys_from_list_of_objects(lectures)

        keys['books'] = material_keys_from_list_of_objects(books)

        keys["theory_images"] = audio_images_keys_from_list_of_objects(theory_images)
        keys["theory_audio"] = audio_images_keys_from_list_of_objects(theory_audio)
        keys["practice_images"] = audio_images_keys_from_list_of_objects(practice_images)
        keys["practice_audio" ] = audio_images_keys_from_list_of_objects(practice_audio)

        return keys















# ####
# REMOVE ?!!!!!!
# ####


    def compare(self, *, db_list_of_keys, cdn_list_of_keys) -> None:
        """
        Accepts list of Dict with key = 'Key' and value = object_key
        to be compared against self.__KEYS

        Returns tuple (checked, extra_list, extra_cdn)

        checked - keys present in both list and self.__KEYS
        extra_list - keys present in list but not in self.__KEYS
        """

        checked = []
        extra_list = []

        for key_object in cdn_list_of_keys:
            if key_object in db_list_of_keys:
                checked.append(key_object)
                db_list_of_keys.remove(key_object)
            

        extra_list = db_list_of_keys

        # TODO: filter out folders

        return (checked, extra_list)
