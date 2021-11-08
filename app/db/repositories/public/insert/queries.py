from typing import List

from app.db.repositories.parsers import string_or_null, list_to_string

from app.models.private import PresentationMediaCreate

def insert_game_query(name_ru, url, description, object_key) -> str:
    return \
        f"SELECT (public.insert_game({string_or_null(name_ru, url, description, object_key)})).*"

def insert_video_query(name_ru, url, description, object_key) -> str:
    return \
        f"SELECT (public.insert_video({string_or_null(name_ru, url, description, object_key)})).*"

def insert_intro_video_query(name_ru, url, description, object_key) -> str:
    return \
        f"SELECT (public.insert_intro_video({string_or_null(name_ru, url, description, object_key)})).*"

def insert_book_query(name_ru, url, description, object_key) -> str:
    return \
        f"SELECT (public.insert_book({string_or_null(name_ru, url, description, object_key)})).*"

def insert_presentation_query(table, name_ru, description, object_key) -> str:
    return \
        f"SELECT (public.insert_{table}({string_or_null(name_ru, description, object_key)})).*"
    
def insert_presentation_media_query(table, media_type , medium: List[PresentationMediaCreate]) -> str:
    """Creates insert query for presentation data.

    table      -- table we are trying to insert into. (practice || theory)
    media_type -- presentation content type (image || audio)
    medium     -- List of PresentationMediaCreate
    """
    order_numbers, urls, keys = map(list, zip( *((media.order, media.url, media.object_key) for media in medium)))

    order_numbers = ','.join(map(str,order_numbers))
    urls = ','.join(map(str,urls))
    keys = ','.join(map(str,keys))

    return \
        f"SELECT (public.insert_{table}_{media_type}('{{{order_numbers}}}'::int[], '{{{urls}}}'::text[], '{{{keys}}}'::text[])).*"

def insert_quiz_question_query(order_number: int, question: str, object_key: str, image_url: str, answers: List[str], is_true: List[bool]) -> str:
    answers = list_to_string(answers)
    is_true = list_to_string(is_true)
    return \
        f"SELECT (public.insert_quiz_question({order_number}, {string_or_null(question, object_key, image_url)}, '{{{answers}}}', '{{{is_true}}}')).*"


# AboutUs, FAQ, Instructions
def insert_about_us_query(order, title, description, svg) -> str:
    return \
        f"SELECT (public.insert_about_us({order}, {string_or_null(title, description, svg)})).*"

def insert_faq_query(question, answer) -> str:
    return \
        f"SELECT (public.insert_faq({string_or_null(question, answer)})).*"

def insert_instruction_query(order, title, description) -> str:
    return \
        f"SELECT (public.insert_instruction({order}, {string_or_null(title, description)})).*"

def insert_review_query(name: str, review: str, object_key: str, image_url: str) -> str:
    return \
        f"SELECT (public.insert_review({string_or_null(name, review, object_key, image_url)})).*"
