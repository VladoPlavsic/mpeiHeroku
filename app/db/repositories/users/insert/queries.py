from app.db.repositories.parsers import string_or_null

def register_new_user_query(full_name, email, phone_number, city, school, salt, password) -> str:
    return \
        f"SELECT (users.create_user_function({string_or_null(full_name, email, phone_number, city, school, salt, password)})).*"

def set_jwt_token_query(user_id, token) -> str:
    return \
        f"SELECT users.set_jwt_token({user_id}, {string_or_null(token)})"

def verify_email_query(user_id) -> str:
    return \
        f"SELECT users.verify_email({user_id})"

def set_confirmation_code_query(user_id, confirmation_code) -> str:
    return \
        f"SELECT users.set_confirmation_code({user_id}, {string_or_null(confirmation_code)}) AS code"


def add_grade_to_user_query(user_id: int, grade_id: int, subscription_fk: int) -> str:
    return \
        f"SELECT (users.add_grade_to_user({user_id}, {grade_id}, {subscription_fk})).*"

def add_subject_to_user_query(user_id, subject_id, subscription_fk: int) -> str:
    return \
        f"SELECT (users.add_subject_to_user({user_id}, {subject_id}, {subscription_fk})).*"

