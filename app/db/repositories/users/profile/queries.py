from app.db.repositories.parsers import string_or_null

def deactivate_profile_query(user_id: int) -> str:
    return \
        f"SELECT users.deactivate_profile({user_id})"

def delete_profile_query(user_id: int) -> str:
    return \
        f"SELECT users.delete_profile({user_id})"

def select_deactivated_profiles_for_warning_month_query() -> str:
    return \
        f"SELECT * FROM users.profiles_for_warning_month_view"


def select_deactivated_profiles_for_warning_week_query() -> str:
    return \
        f"SELECT * FROM users.profiles_for_warning_week_view"


def select_deactivated_profiles_for_deletion_query() -> str:
    return \
        f"SELECT * FROM users.profiles_for_deletion_view"

def create_reactivation_request_query(user_id: int) -> str:
    return \
        f"SELECT users.create_reactivation_request({user_id}) AS reactivation_hash"

def activate_profile_query(reactivation_hash: str) -> str:
    return \
        f"SELECT users.activate_profile({string_or_null(reactivation_hash)}) AS activated"
