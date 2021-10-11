from app.db.repositories.parsers import string_or_null, list_to_string

def update_video_query(name_ru, description) -> str:
    return \
        f"SELECT (public.update_video({string_or_null(name_ru, description)})).*"

def update_intro_video_query(name_ru, description) -> str:
    return \
        f"SELECT (public.update_intro_video({string_or_null(name_ru, description)})).*"

def update_game_query(name_ru, description) -> str:
    return \
        f"SELECT (public.update_game({string_or_null(name_ru, description)})).*"

def update_book_query(name_ru, description) -> str:
    return \
        f"SELECT (public.update_book({string_or_null(name_ru, description)})).*"

def update_presentation_query(presentation, name_ru, description) -> str:
    return \
        f"SELECT (public.update_{presentation}_metadata({string_or_null(name_ru, description)})).*"
 
def update_about_us_query(order, title, description, svg) -> str:
    return \
        f"SELECT (public.update_about_us({order}, {string_or_null(title, description, svg)})).*"

def update_instruction_query(order, title, description) -> str:
    return \
        f"SELECT (public.update_instruction({order}, {string_or_null(title, description)})).*"

def update_faq_query(id, question, answer) -> str:
    return \
        f"SELECT (public.update_faq({id}, {string_or_null(question, answer)})).*"

# link updating
def update_book_links_query(keys, links) -> str:
    keys = list_to_string(keys)
    links = list_to_string(links)
    return \
        f"SELECT public.update_book_links('{{{keys}}}', '{{{links}}}')"

def update_video_links_query(keys, links) -> str:
    keys = list_to_string(keys)
    links = list_to_string(links)
    return \
        f"SELECT public.update_video_links('{{{keys}}}', '{{{links}}}')"

def update_intro_video_links_query(keys, links) -> str:
    keys = list_to_string(keys)
    links = list_to_string(links)
    return \
        f"SELECT public.update_intro_video_links('{{{keys}}}', '{{{links}}}')"

def update_game_links_query(keys, links) -> str:
    keys = list_to_string(keys)
    links = list_to_string(links)
    return \
        f"SELECT public.update_game_links('{{{keys}}}', '{{{links}}}')"

def update_quiz_links_query(keys, links) -> str:
    keys = list_to_string(keys)
    links = list_to_string(links)
    return \
        f"SELECT public.update_quiz_links('{{{keys}}}', '{{{links}}}')"

def update_presentation_part_links_query(keys, links, presentation, media_type) -> str:
    keys = list_to_string(keys)
    links = list_to_string(links)
    return \
        f"SELECT public.update_{presentation}_{media_type}_links('{{{keys}}}', '{{{links}}}')"
