from app.db.repositories.parsers import list_to_string, string_or_null

def update_team_member_photos_query(photo_keys, photo_links) -> str:
    photo_keys = list_to_string(list_=photo_keys)
    photo_links = list_to_string(list_=photo_links)
    return \
        f"SELECT (about.update_team_member_photos('{{{photo_keys}}}'::text[],'{{{photo_links}}}'::text[]))"

def update_team_member_query(id, order, name, role, profession, photo_key, photo_link, description) -> str:
    if description == None:
        description = 'null'
    else:
        description = f"'{description}'"
    return \
        f"SELECT (about.update_team_member({id}, {string_or_null(order, name, role, profession, photo_key, photo_link)}, {description})).*"

def update_contact_query(id, order, html) -> str:
    return \
        f"SELECT (about.update_contact({id}, {string_or_null(order, html)})).*"

def update_about_project_query(id, order, html) -> str:
    return \
        f"SELECT (about.update_about_project({id}, {string_or_null(order, html)})).*"