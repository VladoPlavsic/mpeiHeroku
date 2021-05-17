def get_user_by_email_query(email) -> str:
    return \
        f"SELECT (users.get_user_by_email('{email}')).*"

def get_user_by_username_query(username) -> str:
    return \
        f"SELECT (users.get_user_by_username('{username}')).*"

def set_confirmation_code_query(user_id, confirmation_code) -> str:
    return \
        f"SELECT users.set_confirmation_code({user_id}, '{confirmation_code}')"