def select_all_team_members_query() -> str:
    return \
        f"SELECT (about.select_all_team_members()).*"

def select_all_about_project_query() -> str:
    return \
        f"SELECT (about.select_all_about_project()).*"

def select_all_contacts_query() -> str:
    return \
        f"SELECT (about.select_all_contacts()).*"
