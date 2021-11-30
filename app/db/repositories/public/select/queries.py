from app.db.repositories.parsers import list_to_string

def select_material_query(table) -> str:
    return \
        f"SELECT (public.select_{table}()).*"

def select_intro_video_query() -> str:
    return \
        f"SELECT (public.select_intro_video()).*"

def select_material_parts_query(presentation, media_type) -> str:
    return \
        f"SELECT (public.select_{presentation}_{media_type}()).*"

def select_quiz_questions_query() -> str:
    return \
        f"SELECT (public.get_quiz_questions()).*"

def select_quiz_answers_query(fk) -> str:
    return \
        f"SELECT (public.get_quiz_answers({fk})).*"

def check_quiz_results_query(questions, answers) -> str:
    questions = list_to_string(questions)
    answers = list_to_string(answers)
    return \
        f"SELECT * FROM public.check_quiz_success('{{{questions}}}'::int[], '{{{answers}}}'::int[]) AS (correct boolean[], answers text[], correct_answers text[], correct_answers_id int[], question_ids int[], answer_ids int[], question_numbers int[])"

def select_about_us_query() -> str:
    return \
        f"SELECT (public.select_about_us()).*"

def select_instruction_query() -> str:
    return \
        f"SELECT (public.select_instruction()).*"

def select_faq_query(offset=0, limit=None) -> str:
    limit = limit if limit else 'null'
    return \
        f"SELECT (public.select_faq({offset}, {limit})).*"

def select_all_material_keys_query(table) -> str:
    return \
        f"SELECT public.select_all_{table}_keys() AS object_key"

def select_all_material_part_keys_query(presentation, media_type) -> str:
    return \
        f"SELECT (public.select_all_{presentation}_{media_type}_keys()).*"

def select_all_reviews_query() -> str:
    return \
        f"SELECT (public.select_all_reviews()).*"

def select_titles_query() -> str:
    return \
        f"SELECT (public.get_front_page_titles()).*"


