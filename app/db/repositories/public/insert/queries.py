from typing import List

from app.models.private import PresentationMediaCreate

def insert_game_query(name_ru, url, description) -> str:
    return \
        f"SELECT (public.insert_game('{name_ru}','{url}','{description}')).*"

def insert_video_query(name_ru, url, description) -> str:
    return \
        f"SELECT (public.insert_video('{name_ru}', '{url}', '{description}')).*"

def insert_book_query(name_ru, url, description, key) -> str:
    return \
        f"SELECT (public.insert_book('{name_ru}','{url}', '{description}', '{key}')).*"

def insert_presentation_query(name_ru, description, key, presentation) -> str:
    return \
        f"SELECT (public.insert_{presentation}('{name_ru}', '{description}', '{key}')).*"
    
def insert_presentation_media_query(presentation, media_type , medium: List[PresentationMediaCreate]) -> str:
    '''
    presentation: theory | practice
    media_type: image | audio
    medium: List of PresentationMediaCreate -> url, order, key
        url: sharing link
        order: order number in which it should be displayed when forming presentation
        key: cdn image key
    '''
    order_numbers, urls, keys = map(list, zip( *((media.order, media.url, media.key) for media in medium)))

    order_numbers = ','.join(map(str,order_numbers))
    urls = ','.join(map(str,urls))
    keys = ','.join(map(str,keys))

    return \
        f"SELECT (public.insert_{presentation}_{media_type}('{{{order_numbers}}}'::int[], '{{{urls}}}'::text[], '{{{keys}}}'::text[])).*"



# AboutUs, FAQ, Instructions

def insert_about_us_query(order_num, title, description, svg) -> str:
    return \
        f"SELECT (public.insert_about_us({order_num}, '{title}', '{description}', '{svg}')).*"

def insert_faq_query(question, answer) -> str:
    return \
        f"SELECT (public.insert_faq('{question}', '{answer}')).*"

def insert_instruction_query(order_num, title, description) -> str:
    return \
        f"SELECT (public.insert_instruction({order_num}, '{title}', '{description}')).*"