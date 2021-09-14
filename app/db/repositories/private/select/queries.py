from app.db.repositories.parsers import list_to_string, string_or_null

def select_grades_query(identifications=None) -> str:
    if identifications:
        available = ','.join(map(str,identifications))
        return \
            f"SELECT (private.select_grades_by_ids('{available}')).*"
    else:
        return \
            f"SELECT (private.select_all_grades()).*"

def select_all_grade_keys_query() -> str:
    return \
        f"SELECT (private.select_all_grade_keys()).*"

def get_grade_by_name_query(grade_name) -> str:
    return \
        f"SELECT (private.select_grade_by_name('{grade_name}')).*"

# subject
def select_subject_query(fk, identifications=[]) -> str:
    if identifications:
        available = ','.join(map(str,identifications))
        return \
            f"SELECT (private.select_subjects_by_ids('{available}', {fk})).*"
    else:
        return \
            f"SELECT (private.select_all_subjects({fk})).*"

def select_all_subject_keys_query() -> str:
    return \
        f"SELECT (private.select_all_subject_keys()).*"

def get_subject_by_name_query(fk, subject_name) -> str:
    return \
        f"SELECT (private.select_subject_by_name('{subject_name}', {fk})).*"


# branch
def select_branch_query(fk) -> str:
    return \
        f"SELECT (private.select_all_branches({fk})).*"

def select_all_branch_keys_query() -> str:
    return \
        f"SELECT (private.select_all_branch_keys()).*"

def get_branch_by_name_query(fk, branch_name) -> str:
    return \
        f"SELECT (private.select_branch_by_name('{branch_name}', {fk})).*"


# lecture
def select_lecture_query(fk) -> str:
    return \
        f"SELECT (private.select_all_lectures({fk})).*"

def select_all_lecture_keys_query() -> str:
    return \
        f"SELECT (private.select_all_lecture_keys()).*"

def get_lecture_by_name_query(fk, lecture_name) -> str:
    return \
        f"SELECT (private.select_lecture_by_name('{lecture_name}', {fk})).*"


# ###
# material queries
# ###
def select_material_query(fk) -> str:
    return \
        f"SELECT (private.select_material({fk})).*"

def select_one_material_query(fk, table) -> str:
    return \
        f"SELECT (private.select_{table}({fk})).*"

def select_quiz_questions_query(fk) -> str:
    return \
        f"SELECT (private.get_quiz_questions({fk})).*"

def select_quiz_answers_query(fk) -> str:
    return \
        f"SELECT (private.get_quiz_answers({fk})).*"

def check_quiz_results_query(questions, answers) -> str:
    questions = list_to_string(questions)
    answers = list_to_string(answers)
    return \
        f"SELECT * FROM private.check_quiz_success('{{{questions}}}'::int[], '{{{answers}}}'::int[]) AS (correct boolean[], answers text[], correct_answers text[], correct_answers_id int[], question_ids int[], answer_ids int[], question_numbers int[])"

def select_all_material_keys_query(table) -> str:
    return \
        f"SELECT (private.select_all_{table}_keys()).*"

# material parts
def select_material_parts_query(fk, presentation, media_type) -> str:
    return \
        f"SELECT (private.select_{presentation}_{media_type}({fk})).*"

def select_all_material_part_keys_query(presentation, media_type) -> str:
    return \
        f"SELECT (private.select_all_{presentation}_{media_type}_keys()).*"


# users
def select_all_user_available_grades_query(user_id: int) -> str:
    return \
        f"SELECT (users.select_all_user_available_grades({user_id})).*"

def select_all_user_available_subjects_query(user_id: int) -> str:
    return \
        f"SELECT (users.select_all_user_available_subjects({user_id})).*"

def check_if_content_available_query(user_id: int, grade_name: str, subject_name: str) -> str:
    return \
        f"SELECT users.check_if_content_available({user_id}, {string_or_null(grade_name, subject_name)}) AS available"

# subscriptions
# plans
def get_available_grade_plans_query() -> str:
    return \
        f"SELECT (subscriptions.get_available_grade_plans()).*"

def get_available_subject_plans_query() -> str:
    return \
        f"SELECT (subscriptions.get_available_subject_plans()).*"

# offers
def get_available_grade_offers_query() -> str:
    return \
        f"SELECT (subscriptions.get_available_grade_offers()).*"

def get_available_subject_offers_query() -> str:
    return \
        f"SELECT (subscriptions.get_available_subject_offers()).*"