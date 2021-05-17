from typing import List, Tuple

from app.models.private import StructureAllModel
from app.models.private import MaterialAllModel
from app.models.private import AudioImagesAllModel
from app.models.about import TeamMemberInDBModel
from app.models.news import NewsImagesAllModel

def get_specific_keys_from_content_list(content_list, **kwargs) -> List:
        '''
            Accept raw list of content
            Return list with only speficic keys
            
            Available keys:
                'Key'
                'LastModified'
                'ETag'
                'Size'
                'StorageClass'
        '''

        object_data = {}
        parsed = []
        for content in content_list:
            for key, value in kwargs.items():
                if value == True:
                    object_data[key] = content[key]
            parsed.append(object_data)
            object_data = {}
    
        return parsed


def get_names_from_keys(content_list) -> List:
    '''
        Accepts
            List of Dicts:
                [{
                    Key: "some/key/here/image.jpg"
                }]

        Returns:
            Dict:
                {
                    "some/key/here/image.jpg" : "image.jpg"
                }
    '''

    parsed = {}
    for content in content_list:
        name = content['Key'].split('/')[-1]
        if '.' in name:
            parsed[content['Key']] = name

    return parsed

def get_order_from_keys(content_list) -> Tuple:
    '''
        Accepts
            List of Dicts:
                [{
                    Key: "some/key/here/0001.jpg"
                }]

        Returns:
            Tuple(
                Dict:
                    {
                        "some/key/here/0001.jpg" : 1
                    }
                List:
                    Dict: 
                        {
                            'Key': "some/key/here/image.jpg"
                        }
            )
    '''

    parsed = {}
    delete = {}
    for_deletion = []
    for content in content_list:
        name = content['Key'].split('/')[-1]
        if '.' in name:
            try:
                parsed[content['Key']] = int(name.split('.')[0])
            except:
                delete['Key'] = content['Key'] 
                for_deletion.append(delete)
                delete = {}

    return (parsed, for_deletion)

def filter_prefix(prefix, content_list, exclude_root=True) -> List:
    '''
    Filters list of elements by prefix

        :params:
            prefix - prefix to filter by
            content_list - list to filter
            exclude_root: True - exclude root directory

    Returns list of Dict:
        [
            {
                'Key' : 'object_key_in_cdn'
            }
        ]
    '''
    filtered = []
    prefix = prefix if prefix[-1] == '/' else prefix + '/'
    for content in content_list:
        if prefix in content['Key']:
            if not exclude_root:
                filtered.append(content)
            elif prefix != content['Key']:
                filtered.append(content)

    return filtered


def list_root_directory_files(prefix, content_list, exclude_root=True, exclude_files=[]) -> List:
    '''
    Return only files from directory

        :params:
            prefix - directory prefix to filter
            content_list - list to filter
            exclude_root: True - exclude directory itself
            exclude_files: List of filed to be excluded by key
    Returns list of Dict:
        [
            {
                'Key' : 'object_key_in_cdn'
            }
        ]
    '''
    filtered = []
    prefix = prefix if prefix[-1] == '/' else prefix + '/'
    
    for content in content_list:
        if prefix in content['Key'] and prefix != content['Key']:
            if '/' not in content['Key'].split(prefix)[1]:
                if content['Key'] not in exclude_files:
                    filtered.append(content)
                elif not exclude_files:
                    filtered.append(content)

    if not exclude_root:
        filtered.append({"Key": prefix})

    return filtered


def check_key_exists_in_list_of_objects(key, list_of_objects) -> bool:

        for object_key in list_of_objects:
            if key == object_key['Key']:
                return True

        print(f"Didn't find key {key} in \n {list_of_objects}")        
        return False

def get_prefix_by_inner_key(key: str) -> str:

    sufix = key.split("/")[-1]
    
    return key.replace(sufix, '')

def structure_keys_from_list_of_objects(list_: List[StructureAllModel]):
    list_of_keys = [{"Key": structure_object.background_key} for structure_object in list_]

    return list_of_keys

def material_keys_from_list_of_objects(list_: List[MaterialAllModel]):
    list_of_keys = [{"Key": material_object.key} for material_object in list_]

    return list_of_keys

def audio_images_keys_from_list_of_objects(list_: List[AudioImagesAllModel]):
    list_of_keys = [{"Key": media_object.key} for media_object in list_]

    return list_of_keys

def news_images_keys_from_list_of_objects(list_: List[NewsImagesAllModel]):
    list_of_keys = [{"Key": media_object.cloud_key} for media_object in list_]

    return list_of_keys

def team_member_keys_from_list_of_objects(list_: List[TeamMemberInDBModel]):
    list_of_keys = [{"Key": team_member.photo_key} for team_member in list_]

    return list_of_keys