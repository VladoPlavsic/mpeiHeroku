from app.db.repositories.parsers import string_or_null

def update_user_information_query(id_: int, full_name: str, phone_number: str, city: str, school: str):
    return \
        f"SELECT (users.update_personal_information({id_}, {string_or_null(full_name, phone_number, city, school)})).*"
