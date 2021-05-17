def delete_grade_query(id) -> str:
    return \
        f"SELECT private.delete_grade_by_id({id}) AS key"

def delete_subject_query(id) -> str:
    return \
        f"SELECT private.delete_subject_by_id({id}) AS key"

def delete_branch_query(id) -> str:
    return \
        f"SELECT private.delete_branch_by_id({id}) AS key"

def delete_lecture_query(id) -> str:
    return \
        f"SELECT private.delete_lecture_by_id({id}) AS key"

def delete_theory_query(id) -> str:
    return \
        f"SELECT private.delete_theory_by_id({id}) AS key"

def delete_practice_query(id) -> str:
    return \
        f"SELECT private.delete_practice_by_id({id}) AS key"

def delete_book_query(id) -> str:
    return \
        f"SELECT private.delete_book_by_id({id}) AS key"

def delete_video_query(id) -> str:
    return \
        f"SELECT private.delete_video_by_id({id}) AS key"

# we don't need to return anything from these
def delete_game_query(id) -> str:
    return \
        f"SELECT private.delete_game_by_id({id})"