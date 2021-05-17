def delete_video_query() -> str:
    return \
        f"SELECT public.delete_video()"

def delete_book_query() -> str:
    return \
        f"SELECT public.delete_book() AS key"

def delete_game_query() -> str:
    return \
        f"SELECT public.delete_game()"

def delete_theory_query() -> str:
    return \
        f"SELECT public.delete_theory() AS key"

def delete_practice_query() -> str:
    return \
        f"SELECT public.delete_practice() AS key"

def delete_about_us_query(order_number) -> str:
    return \
        f"SELECT public.delete_about_us({order_number})" 

def delete_faq_query(id) -> str:
    return \
        f"SELECT public.delete_faq({id})"

def delete_instruction_query(order_number) -> str:
    return \
        f"SELECT public.delete_instruction({order_number})"