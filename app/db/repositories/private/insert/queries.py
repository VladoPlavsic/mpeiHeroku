from typing import List

from app.models.private import PresentationMediaCreate

import logging

logger = logging.getLogger(__name__)



# ###
# Structure queries
# ###

def insert_grades_query(name_en, name_ru, background_key, background) -> str:
    return \
        f"SELECT (private.insert_grade('{name_en}', '{name_ru}', '{background_key}', '{background}')).*"
        

def insert_subject_query(fk, name_en, name_ru, background_key, background) -> str:
    return \
        f"SELECT (private.insert_subject({fk}, '{name_en}', '{name_ru}', '{background_key}', '{background}')).*"

def insert_branch_query(fk, name_en, name_ru, background_key, background) -> str:
    return \
        f"SELECT (private.insert_branch({fk}, '{name_en}', '{name_ru}', '{background_key}', '{background}')).*"

def insert_lecture_query(fk, name_en, name_ru, description, background_key, background) -> str:
    return \
        f"SELECT (private.insert_lecture({fk}, '{name_en}', '{name_ru}', '{description}', '{background_key}', '{background}')).*"

# ###
# Material queries
# ###

def insert_video_query(fk, name_ru, description, key, url) -> str:
    return \
        f"SELECT (private.insert_video({fk}, '{name_ru}', '{description}', '{key}', '{url}')).*"

def insert_game_query(fk, name_ru, description, url) -> str:
    return \
        f"SELECT (private.insert_game({fk}, '{name_ru}', '{description}', '{url}')).*"

def insert_book_query(fk, name_ru, description, key, url) -> str:
    return \
        f"SELECT (private.insert_book({fk}, '{name_ru}', '{description}', '{key}', '{url}')).*"

def insert_presentation_query(presentation, fk, name_ru, description, key) -> str:
    '''
    presentation: theory | practice
    fk: lecture id (id of lecture we are adding material to)
    name_ru: presentation name
    description: presentation description
    key: presentation key in cdn
    '''

    return \
        f"SELECT (private.insert_{presentation}({fk}, '{name_ru}', '{description}', '{key}')).*"

def insert_presentation_media_query(presentation, media_type , medium: List[PresentationMediaCreate]) -> str:
    '''
    presentation: theory | practice
    media_type: image | audio
    medium: List of PresentationMediaCreate -> fk, url, order
        fk: id of lecture we are adding to
        url: sharing link
        order: order number in which it should be displayed when forming presentation
    '''
    foreign_keys, order_numbers, urls, keys = map(list, zip( *((media.fk, media.order, media.url, media.key) for media in medium)))

    foreign_keys = ','.join(map(str,foreign_keys))
    order_numbers = ','.join(map(str,order_numbers))
    urls = ','.join(map(str,urls))
    keys = ','.join(map(str,keys))

    return \
        f"SELECT (private.insert_{presentation}_{media_type}('{{{foreign_keys}}}'::int[], '{{{order_numbers}}}'::int[], '{{{urls}}}', '{{{keys}}}')).*"


# timestamp
def check_timestamp_is_set_query() -> str:
    return "SELECT COUNT(*) AS count FROM private.timestamp;"

def set_timestamp_to_now_query() -> str:
    return "INSERT INTO private.timestamp(last_update, is_updating)  VALUES(now(), 'f');"