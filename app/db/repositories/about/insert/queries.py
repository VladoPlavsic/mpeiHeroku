from app.db.repositories.parsers import string_or_null

def insert_our_team_query(order, name, role, profession, description, photo_key, photo_link) -> str:
    return \
        f"SELECT (about.insert_our_team({order}, {string_or_null(name, role, profession, description, photo_key, photo_link)})).*"

def insert_about_project_query(order, html) -> str:
    return \
        f"SELECT (about.insert_about_project({order}, {string_or_null(html)})).*"

def insert_contacts_query(order, html) -> str:
    return \
        f"SELECT (about.insert_contacts({order}, {string_or_null(html)})).*"
