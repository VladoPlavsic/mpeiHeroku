def delete_team_member_query(id) -> str:
    return \
        f"SELECT about.delete_team_member({id}) AS deleted"

def delete_about_project_query(id) -> str:
    return \
        f"SELECT (about.delete_about_project({id}))"

def delete_contact_query(id) -> str:
    return \
        f"SELECT (about.delete_contact({id}))"
