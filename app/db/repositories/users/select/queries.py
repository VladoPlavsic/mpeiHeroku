from app.db.repositories.parsers import string_or_null

def get_user_by_email_query(email) -> str:
    return \
        f"SELECT (users.get_user_by_email({string_or_null(email)})).*"

def get_user_by_id_query(user_id) -> str:
    return \
        f"SELECT (users.get_user_by_id({user_id})).*"

def get_user_by_username_query(username) -> str:
    return \
        f"SELECT (users.get_user_by_username({string_or_null(username)}).*"

def check_confirmation_code_query(user_id: int, confirmation_code) -> str:
    return \
        f"SELECT users.check_confirmation_code({user_id}, {string_or_null(confirmation_code)}) AS valid"

def get_grade_subscription_history_query(user_id: int) -> str:
    return \
        f"SELECT (history.get_grade_subscription_history({user_id})).*"

def get_subject_subscription_history_query(user_id: int) -> str:
    return \
        f"SELECT (history.get_subject_subscription_history({user_id})).*"
