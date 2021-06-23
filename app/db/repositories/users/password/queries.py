from app.db.repositories.parsers import string_or_null

def reset_password_request_query(email: str) -> str:
    return \
        f"SELECT users.create_recovery_request({string_or_null(email)}) AS recovery_key"

def confirm_password_recovery_query(email: str, recovery_key: str) -> str:
    return \
        f"SELECT users.check_recovery_request({string_or_null(email, recovery_key)}) AS recovery_hash"

def recover_password_query(hash_: str, password: str, salt: str) -> str:
    return \
        f"SELECT users.update_password({string_or_null(hash_, password, salt)}) AS updated"
