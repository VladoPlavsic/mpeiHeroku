"""This module is connecting our server to Yandex.Cloud s3 API using boto3.
 
In particular this module uses only S3 service.
boto3 documentation: https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
boto3 S3 service docmuentation: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
"""
import boto3
from typing import List, Dict
# exceptions
from fastapi import HTTPException
from botocore.errorfactory import ClientError

# config
from app.core.config import BUCKET, CDN_LINK_LIFESPAN
from app.cdn.types import DefaultFolders, DefaultFormats, ObjectTypes

# models
from app.models.private import PresentationMediaCreate
from app.models.private import StructureAllModel
from app.models.private import MaterialAllModel
from app.models.private import AudioImagesAllModel

# parsers
from app.cdn.repositories.parsers import get_order_number_from_key, get_format_from_key, get_folder_by_inner_key

import logging

logger = logging.getLogger(__name__)

class BaseCDNRepository:
    """Class connecting Yandex.Cloud s3 with our server. 
    
    Implementing logic for getting presingend link (sharing content) from items stored in s3 cloud.
    To be inherited by specific classes depending on extra functionality needed.
    """
    def __init__(self, client: boto3.client) -> None:
        """Accepts new boto3 s3 client and stores it in current object for future uses."""
        self.client = client

    def __list_objects(self, prefix: str = '', continuation_token: str = ''):
        """Lists bucket based of prefix and continuation token. Return all keys from bucket with prefix"""
        response = []
        try:
            raw_response = self.client.list_objects_v2(Bucket=BUCKET, Prefix=prefix, ContinuationToken=continuation_token)
            # Create list of keys from raw response (https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_objects_v2)
            response.extend([content['Key'] for content in raw_response['Contents']])
            # Recursivly get all content while IsTruncated
            if raw_response['IsTruncated']:
                response.extend(self.__list_objects(prefix=prefix, continuation_token=raw_response['NextContinuationToken']))

        except Exception as e:
            logger.error("--- LIST BUCKET OBJECTS ERROR ---")
            logger.error(e)
            logger.error("--- LIST BUCKET OBJECTS ERROR ---")

        return response

    def __list_folder(self, folder: str) -> List[str]:
        """Accepts folder (path to folder in s3) and returns list of all keys in that folder."""
        if folder[-1] != '/': # make sure there is / at the end of folder key
            folder += '/'

        return self.__list_objects(prefix=folder)

    def __share_key_content(self, key: str) -> List[str]:
        """Accepts one key and creates presigned url for it. Returns {key: url} pair.
        
        If the key doesn't exist in s3 warning will be logged and None returned.
        """
        try:
            self.client.head_object(Bucket=BUCKET, Key=key) # if element doesn't exist this will raise ClientErro exception
            presigned_url = self.client.generate_presigned_url('get_object', Params={'Bucket': BUCKET, 'Key': key}, ExpiresIn=CDN_LINK_LIFESPAN)
        except ClientError:
            logger.warn("--- EXCEPTION GENERATING PRESIGNED URL ---")
            logger.warn(f"404 - Key not found. Key: {key}")
            logger.warn("--- EXCEPTION GENERATING PRESIGNED URL ---")
            return None
        
        return {key: presigned_url}

    def __get_presigned_links_from_list_of_keys(self, list_of_keys: List[str]):
        """Accepts list of keys to generate presigned links for. Returns list of {key: url} pairs."""
        shared = []
        for key in list_of_keys:
            element = self.__share_key_content(key=key)
            if element:
                shared.append(element)

        return shared

    def __share_folder_content(self, folder_key: str) -> List[str]:
        """Accepts folder key (path to folder in s3) and return list of {key: url} pairs."""
        keys = self.__list_folder(folder=folder_key)
        return self.__get_presigned_links_from_list_of_keys(list_of_keys=keys)

    def __share_data(self, *, folder: str, type_: DefaultFormats) -> List[Dict[str, str]]:
        """Accept folder containing data. Create sharing links for items in that folder if suported format.
        
        Keyword arguments:
        folder -- folder at which our content is located
        type_  -- format type. Used to figure out which content we want to create
        """
        if folder[-1] != '/': # make sure there is / at the end of folder key
            folder += '/'

        if type_ == DefaultFormats.IMAGES:
            folder += DefaultFolders.IMAGES.value
        elif type_ == DefaultFormats.AUDIO:
            folder += DefaultFolders.AUDIO.value

        suported_formats = type_.value
        # exclude keys with unsuported formats and delete them
        shared = [
            item for item in self.__share_folder_content(folder_key=folder) \
                if get_format_from_key(list(item.keys())[0]) in type_.formats
            ]

        if not shared and type_ != DefaultFormats.AUDIO:
            raise HTTPException(status_code=404, detail=f"No valid keys found in folder {folder}")

        return shared

    def __grant_public_access_to_list_of_keys(self, *, list_of_keys) -> None:
        """Grants public access to keys passed in a list."""
        for key in list_of_keys:
            self.client.put_object_acl(Bucket=BUCKET, Key=key, ACL="public-read")


    def __grant_public_access_to_folder_objects(self, *, folder, exclude = []) -> None:
        """Grants public access to all objects in a folder.
        
        Keyword arguments:
        folder  -- key of a folder we want to grant public access to objects of which.
        exclude -- list of keys we want to exclude (not grant public access to) in a folder.
        """
        if folder[-1] != '/': # make sure there is / at the end of folder key
            folder += '/'

        object_to_grant_access_to = [
            list(item.keys())[0] for item in self.__share_folder_content(folder_key=folder) \
                if list(item.keys())[0] not in exclude
            ]

        self.__grant_public_access_to_list_of_keys(list_of_keys=object_to_grant_access_to)


    def __delete_keys(self, *, list_of_keys) -> Dict:
        """Delete all keys from s3 contained in list_of_keys."""
        # required format:
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_objects
        keys = [{"Key": key} for key in list_of_keys]
        response = self.client.delete_objects(Bucket=BUCKET, Delete={'Objects': keys, 'Quiet': True})
        return response

    def format_presentation_content(self, *, folder, fk, type_: DefaultFormats) -> List[PresentationMediaCreate]:
        """This function formats presentation content for it to be inserted into database.
        
        Keyword arguments:
        folder -- s3 key containing given lecture data. (e.g. subscriptions/7-9/physics/mechanics/kinematics/practice/)
        fk     -- lecture foreign key
        type_  -- data type. Used for figuring out containing folder for given type

        This function returns List of PresentationMediaCreate. 
        In case there are no images found for given path (if type_ = DefaultFormats.IMAGES)
        HTTPException will be raised, and nothing will be added to database.
        """
        shared = self.__share_data(folder=folder, type_=type_)

        formated = []
        for item in shared:
            key = list(item.keys())[0]
            file_format = get_format_from_key(key=key)
         
            order_number = get_order_number_from_key(key=key)
            if order_number:
                formated.append(PresentationMediaCreate(order=order_number, url=item[key], fk=fk, object_key=key))

        if type_ == DefaultFormats.IMAGES and not formated:
            raise HTTPException(status_code=404, detail=f"No images found a path {folder}. Images must be present!")

        return formated
    
    def form_book_insert_data(self, *, folder) -> List[Dict[str, str]]:
        """This function creates presigned sharing urls for book.
        
        Keyword arguments:
        folder -- s3 key containing given book.
        
        Returns list of dictionaries with:
        key   -- s3 key of a book
        value -- presigned url for given key
        """
        return self.__share_data(folder=folder, type_=DefaultFormats.BOOK)

    def form_video_insert_data(self, *, folder) -> List[Dict[str, str]]:
        """This function creates presigned sharing urls for video.
        
        Keyword arguments:
        folder -- s3 key containing given video.
        
        Returns list of dictionaries with:
        key   -- s3 key of a video
        value -- presigned url for given key
        """
        return self.__share_data(folder=folder, type_=DefaultFormats.VIDEO)

    def form_game_insert_data(self, *, folder) -> List[Dict[str, str]]:
        """This function creates presigned sharing urls for game.

        It also grants public access to all dependency content
        needed for game to load. (e.g. all content of folder build Build)

        Keyword arguments:
        folder -- s3 key containing given game.

        Returns list of dictionaries with:
        key   -- s3 key of a game
        value -- presigned url for given key
        """
        if folder[-1] != '/': # make sure there is / at the end of folder key
            folder += '/'
        self.__grant_public_access_to_folder_objects(folder=folder, exclude=[folder + "index.html", folder])

        return self.__share_data(folder=folder, type_=DefaultFormats.GAME)

    def form_quiz_insert_data(self, *, folder) -> List[Dict[str, str]]:
        """This function creates presigned sharing urls for quiz.
        
        Keyword arguments:
        folder -- s3 key containing given quiz.
        
        Returns list of dictionaries with:
        key   -- s3 key of a quiz
        value -- presigned url for given key
        """
        return self.__share_data(folder=folder, type_=DefaultFormats.QUIZ)

    def delete_key(self, *, key) -> None:
        """Deletes a single object from s3 by it's object_key"""
        response = self.__delete_keys(list_of_keys=[key])
        if "Errors" in response:
            logger.warn("---THERE HAS BEEN SOME ERRORS IN DELETING KEYS---")
            for error in response['Errors']:
                logger.warn(f"Key {error['Key']} has not been deleted.")
                logger.warn(f"s3 said: {error['Message']}")
            logger.warn("---THERE HAS BEEN SOME ERRORS IN DELETING KEYS---")        

    def delete_keys(self, *, list_of_keys) -> None:
        """Deletes all objects from a list of keys"""
        response = self.__delete_keys(list_of_keys=list_of_keys)
        if "Errors" in response:
            logger.warn("---THERE HAS BEEN SOME ERRORS IN DELETING KEYS---")
            for error in response['Errors']:
                logger.warn(f"Key {error['Key']} has not been deleted.")
                logger.warn(f"s3 said: {error['Message']}")
            logger.warn("---THERE HAS BEEN SOME ERRORS IN DELETING KEYS---")        

    def delete_folder_by_inner_key(self, *, inner_key) -> None:
        """Delete folder by any of it's containing keys"""
        folder = get_folder_by_inner_key(key=inner_key)
        self.delete_folder(folder=folder)
    
    def delete_folder(self, *, folder) -> None:
        """Delete folder by it's name (key in s3)"""
        all_keys = self.__list_folder(folder=folder)
        response = self.__delete_keys(list_of_keys=all_keys)
        if "Errors" in response:
            logger.warn("---THERE HAVE BEEN SOME ERRORS IN DELETING KEYS---")
            for error in response['Errors']:
                logger.warn(f"Key {error['Key']} has not been deleted.")
                logger.warn(f"s3 said: {error['Message']}")
            logger.warn("---THERE HAVE BEEN SOME ERRORS IN DELETING KEYS---")

    def get_sharing_links_from_objects(self, *, list_of_objects) -> Dict:
        """Accept objects of any type of content stored in s3.
        
        Converts objects to list of corresponding keys and shares those keys.
        Returns dictionary with:
        key   -- object key in s3
        value -- presigned sharing link
        """
        list_of_keys = [element.object_key for element in list_of_objects]

        shared_list = self.__get_presigned_links_from_list_of_keys(list_of_keys=list_of_keys)

        final = {}        
        for item in shared_list:
            final.update(item)
        return final

    def get_sharing_link_from_object_key(self, *, object_key: str) -> Dict:
        """Accepts single object_key of and object stored in s3.
        
        Returns dictionary like object with:
        key   -- object key in s3
        value -- presigned sharing link
        """

        return self.__share_key_content(key=object_key)