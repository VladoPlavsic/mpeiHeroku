from typing import List

from app.models.private import PresentationMediaCreate
from app.db.repositories.parsers import string_or_null, list_to_string

import logging

logger = logging.getLogger(__name__)

# ###
# Structure queries
# ###

def insert_grades_query(name_en, name_ru, background_key, background, order_number) -> str:
    return \
        f"SELECT (private.insert_grade({string_or_null(name_en, name_ru, background_key, background)}, {order_number})).*"
        

def insert_subject_query(fk, name_en, name_ru, background_key, background, order_number) -> str:
    return \
        f"SELECT (private.insert_subject({fk}, {string_or_null(name_en, name_ru, background_key, background)}, {order_number})).*"

def insert_branch_query(fk, name_en, name_ru, background_key, background, order_number) -> str:
    return \
        f"SELECT (private.insert_branch({fk}, {string_or_null(name_en, name_ru, background_key, background)}, {order_number})).*"

def insert_lecture_query(fk, name_en, name_ru, description, background_key, background, order_number) -> str:
    return \
        f"SELECT (private.insert_lecture({fk}, {string_or_null(name_en, name_ru, description, background_key, background)}, {order_number})).*"

# ###
# Material queries
# ###

def insert_video_query(fk, name_ru, description, key, url) -> str:
    return \
        f"SELECT (private.insert_video({fk}, {string_or_null(name_ru, description, key, url)})).*"

def insert_game_query(fk, name_ru, description, url) -> str:
    return \
        f"SELECT (private.insert_game({fk}, {string_or_null(name_ru, description, url)})).*"

def insert_book_query(fk, name_ru, description, key, url) -> str:
    return \
        f"SELECT (private.insert_book({fk}, {string_or_null(name_ru, description, key, url)})).*"

def insert_presentation_query(presentation, fk, name_ru, description, key) -> str:
    '''
    presentation: theory | practice
    fk: lecture id (id of lecture we are adding material to)
    name_ru: presentation name
    description: presentation description
    key: presentation key in cdn
    '''

    return \
        f"SELECT (private.insert_{presentation}({fk}, {string_or_null(name_ru, description, key)})).*"

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

def insert_quiz_question_query(lecture_id: int, order_number: int, question: str, image_key: str, image_url: str, answers: List[str], is_true: List[bool]) -> str:
    answers = list_to_string(answers)
    is_true = list_to_string(is_true)
    return \
        f"SELECT (private.insert_quiz_question({lecture_id}, {order_number}, {string_or_null(question, image_key, image_url)}, '{{{answers}}}', '{{{is_true}}}')).*"

def insert_quiz_question_answers_query(question_id: int, answers: List[str], is_true: List[bool]) -> str:
    answers = list_to_string(answers)
    is_true = list_to_string(is_true)
    return \
        f"SELECT (private.insert_quiz_answers({question_id}, '{{{answers}}}', '{{{is_true}}}')).*"

# subscriptions
# plans
def insert_available_grade_plans_query(name: str, price: float, month_count: int) -> str:
    return \
        f"SELECT subscriptions.insert_available_grade_plans({string_or_null(name)}, {price}, {month_count})"

def insert_available_subject_plans_query(name: str, price: float, month_count: int) -> str:
    return \
        f"SELECT subscriptions.insert_available_subject_plans({string_or_null(name)}, {price}, {month_count})"


#TODO: Find out if they are still used (I don't think they are)
# timestamp 
def check_timestamp_is_set_query() -> str:
    return "SELECT COUNT(*) AS count FROM private.timestamp;"

def set_timestamp_to_now_query() -> str:
    return "INSERT INTO private.timestamp(last_update, is_updating)  VALUES(now(), 'f');"
