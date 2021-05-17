"""Link updating functions
Revision ID: e012f9ef74b1
Revises: 124a05dc847d
Create Date: 2021-04-01 10:34:55.572569
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = 'e012f9ef74b1'
down_revision = '124a05dc847d'
branch_labels = None
depends_on = None

def create_select_all_keys_from_schema_private_functions():
    # grades
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_all_grade_keys()
        RETURNS TABLE (id int, background_key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT private.grade.id, private.grade.background_key FROM private.grade);
        END $$ LANGUAGE plpgsql;
    """)

    # subject select functions
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_all_subject_keys()
        RETURNS TABLE (id int, background_key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT private.subject.id, private.subject.background_key FROM private.subject);
        END $$ LANGUAGE plpgsql;
    """)

    # branch select functions
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_all_branch_keys()
        RETURNS TABLE (id int, background_key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT private.branch.id, private.branch.background_key FROM private.branch);
        END $$ LANGUAGE plpgsql;
    """)

    # lecture select function
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_all_lecture_keys()
        RETURNS TABLE (id int,  background_key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT private.lecture.id, private.lecture.background_key FROM private.lecture);
        END $$ LANGUAGE plpgsql;
    """)

    # theory
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_all_theory_keys()
        RETURNS TABLE (id int, key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT private.theory.fk, private.theory.key FROM private.theory);
        END $$ LANGUAGE plpgsql;
    """)
    # thoery images
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_all_theory_image_keys()
        RETURNS TABLE ("order" int, key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT private.theory_image."order", private.theory_image.key FROM private.theory_image);
        END $$ LANGUAGE plpgsql;
    """)
    # theory audio
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_all_theory_audio_keys()
        RETURNS TABLE ("order" int, key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT private.theory_audio."order", private.theory_audio.key FROM private.theory_audio);
        END $$ LANGUAGE plpgsql;
    """)
    
    # practice
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_all_practice_keys()
        RETURNS TABLE (id int, key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT private.practice.fk, private.practice.key FROM private.practice);
        END $$ LANGUAGE plpgsql;
    """)
    # practice images
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_all_practice_image_keys()
        RETURNS TABLE ("order" int, key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT private.practice_image."order", private.practice_image.key FROM private.practice_image);
        END $$ LANGUAGE plpgsql;
    """)
    # practice audio
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_all_practice_audio_keys()
        RETURNS TABLE ("order" int, key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT private.practice_audio."order", private.practice_audio.key FROM private.practice_audio);
        END $$ LANGUAGE plpgsql;
    """)

    # video
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_all_video_keys()
        RETURNS TABLE (id int, key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT private.video.fk, private.theory.key FROM private.video);
        END $$ LANGUAGE plpgsql;
    """)
    
    # book
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_all_book_keys()
        RETURNS TABLE (id int, key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT private.book.fk, private.book.key FROM private.book);
        END $$ LANGUAGE plpgsql;
    """)

def create_link_updating_functions_schema_private():
    # grade
    op.execute("""
    CREATE OR REPLACE FUNCTION private.update_grade_links(text[], text[])
        RETURNS VOID
        AS $$
        BEGIN
        FOR index IN 1 .. array_upper($1, 1)
        LOOP
            UPDATE private.grade SET
            background = $2[index] 
            WHERE background_key = $1[index];
        END LOOP;
        END $$ LANGUAGE plpgsql;
    """)
    # subject
    op.execute("""
    CREATE OR REPLACE FUNCTION private.update_subject_links(text[], text[])
        RETURNS VOID
        AS $$
        BEGIN
        FOR index IN 1 .. array_upper($1, 1)
        LOOP
            UPDATE private.subject SET
            background = $2[index] 
            WHERE background_key = $1[index];
        END LOOP;
        END $$ LANGUAGE plpgsql;
    """)
    # branch
    op.execute("""
    CREATE OR REPLACE FUNCTION private.update_branch_links(text[], text[])
        RETURNS VOID
        AS $$
        BEGIN
        FOR index IN 1 .. array_upper($1, 1)
        LOOP
            UPDATE private.branch SET
            background = $2[index] 
            WHERE background_key = $1[index];
        END LOOP;
        END $$ LANGUAGE plpgsql;
    """)
    # lecture
    op.execute("""
    CREATE OR REPLACE FUNCTION private.update_lecture_links(text[], text[])
        RETURNS VOID
        AS $$
        BEGIN
        FOR index IN 1 .. array_upper($1, 1)
        LOOP
            UPDATE private.lecture SET
            background = $2[index] 
            WHERE background_key = $1[index];
        END LOOP;
        END $$ LANGUAGE plpgsql;
    """)
    # theory images
    op.execute("""
    CREATE OR REPLACE FUNCTION private.update_theory_image_links(text[], text[])
        RETURNS VOID
        AS $$
        BEGIN
        FOR index IN 1 .. array_upper($1, 1)
        LOOP
            UPDATE private.theory_image SET
            url = $2[index] 
            WHERE key = $1[index];
        END LOOP;
        END $$ LANGUAGE plpgsql;
    """)
    # theory audio
    op.execute("""
    CREATE OR REPLACE FUNCTION private.update_theory_audio_links(text[], text[])
        RETURNS VOID
        AS $$
        BEGIN
        FOR index IN 1 .. array_upper($1, 1)
        LOOP
            UPDATE private.theory_audio SET
            url = $2[index] 
            WHERE key = $1[index];
        END LOOP;
        END $$ LANGUAGE plpgsql;
    """)
    # practice images
    op.execute("""
    CREATE OR REPLACE FUNCTION private.update_practice_image_links(text[], text[])
        RETURNS VOID
        AS $$
        BEGIN
        FOR index IN 1 .. array_upper($1, 1)
        LOOP
            UPDATE private.practice_image SET
            url = $2[index] 
            WHERE key = $1[index];
        END LOOP;
        END $$ LANGUAGE plpgsql;
    """)
    # practice audio
    op.execute("""
    CREATE OR REPLACE FUNCTION private.update_practice_audio_links(text[], text[])
        RETURNS VOID
        AS $$
        BEGIN
        FOR index IN 1 .. array_upper($1, 1)
        LOOP
            UPDATE private.practice_audio SET
            url = $2[index] 
            WHERE key = $1[index];
        END LOOP;
        END $$ LANGUAGE plpgsql;
    """)
    # book
    op.execute("""
    CREATE OR REPLACE FUNCTION private.update_book_links(text[], text[])
        RETURNS VOID
        AS $$
        BEGIN
        FOR INDEX IN 1 .. array_upper($1, 1)
        LOOP
            UPDATE private.book SET
            url = $2[index]
            WHERE key = $1[index];
        END LOOP;
        END $$ LANGUAGE plpgsql;
    """)


def craete_select_all_keys_from_schema_public_functions():
    # thoery images
    op.execute("""
    CREATE OR REPLACE FUNCTION public.select_all_theory_image_keys()
        RETURNS TABLE ("order" int, key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT public.theory_image."order", public.theory_image.key FROM public.theory_image);
        END $$ LANGUAGE plpgsql;
    """)
    # theory audio
    op.execute("""
    CREATE OR REPLACE FUNCTION public.select_all_theory_audio_keys()
        RETURNS TABLE ("order" int, key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT public.theory_audio."order", public.theory_audio.key FROM public.theory_audio);
        END $$ LANGUAGE plpgsql;
    """)
    # practice images
    op.execute("""
    CREATE OR REPLACE FUNCTION public.select_all_practice_image_keys()
        RETURNS TABLE ("order" int, key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT public.practice_image."order", public.practice_image.key FROM public.practice_image);
        END $$ LANGUAGE plpgsql;
    """)
    # practice audio
    op.execute("""
    CREATE OR REPLACE FUNCTION public.select_all_practice_audio_keys()
        RETURNS TABLE ("order" int, key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT public.practice_audio."order", public.practice_audio.key FROM public.practice_audio);
        END $$ LANGUAGE plpgsql;
    """)    
    # book
    op.execute("""
    CREATE OR REPLACE FUNCTION public.select_all_book_keys()
        RETURNS TABLE (key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT public.book.key FROM public.book);
        END $$ LANGUAGE plpgsql;
    """)


def create_link_updating_functions_schema_public():
    # book
    op.execute("""
    CREATE OR REPLACE FUNCTION public.update_book_links(text[], text[])
        RETURNS VOID
        AS $$
        BEGIN
        FOR INDEX IN 1 .. array_upper($1, 1)
        LOOP
            UPDATE public.book SET
            url = $2[index]
            WHERE key = $1[index];
        END LOOP;
        END $$ LANGUAGE plpgsql;
    """)
    # theory images
    op.execute("""
    CREATE OR REPLACE FUNCTION public.update_theory_image_links(text[], text[])
        RETURNS VOID
        AS $$
        BEGIN
        FOR index IN 1 .. array_upper($1, 1)
        LOOP
            UPDATE public.theory_image SET
            url = $2[index] 
            WHERE key = $1[index];
        END LOOP;
        END $$ LANGUAGE plpgsql;
    """)
    # theory audio
    op.execute("""
    CREATE OR REPLACE FUNCTION public.update_theory_audio_links(text[], text[])
        RETURNS VOID
        AS $$
        BEGIN
        FOR index IN 1 .. array_upper($1, 1)
        LOOP
            UPDATE public.theory_audio SET
            url = $2[index] 
            WHERE key = $1[index];
        END LOOP;
        END $$ LANGUAGE plpgsql;
    """)
    # practice images
    op.execute("""
    CREATE OR REPLACE FUNCTION public.update_practice_image_links(text[], text[])
        RETURNS VOID
        AS $$
        BEGIN
        FOR index IN 1 .. array_upper($1, 1)
        LOOP
            UPDATE public.practice_image SET
            url = $2[index] 
            WHERE key = $1[index];
        END LOOP;
        END $$ LANGUAGE plpgsql;
    """)
    # practice audio
    op.execute("""
    CREATE OR REPLACE FUNCTION public.update_practice_audio_links(text[], text[])
        RETURNS VOID
        AS $$
        BEGIN
        FOR index IN 1 .. array_upper($1, 1)
        LOOP
            UPDATE public.practice_audio SET
            url = $2[index] 
            WHERE key = $1[index];
        END LOOP;
        END $$ LANGUAGE plpgsql;
    """)

def drop_link_updating_functions_schema_private():
    functions = [
        'update_grade_links',
        'update_subject_links',
        'update_branch_links',
        'update_lecture_links',
        'update_practice_image_links',
        'update_practice_audio_links',
        'update_theory_image_links',
        'update_theory_audio_links',
        'update_book_links']

    for function in functions:
        op.execute(f"DROP FUNCTION private.{function}")

def drop_link_updating_functions_schema_public():
    functions = [
        'update_practice_image_links',
        'update_practice_audio_links',
        'update_theory_image_links',
        'update_theory_audio_links',
        'update_book_links']

    for function in functions:
        op.execute(f"DROP FUNCTION public.{function}")

def drop_select_all_keys_from_schema_private_functions():
    functions = [
        "select_all_theory_keys",
        "select_all_theory_image_keys",
        "select_all_theory_audio_keys",
        "select_all_practice_keys",
        "select_all_practice_image_keys",
        "select_all_practice_audio_keys",
        "select_all_video_keys",
        "select_all_book_keys",]

    for function in functions:
        op.execute(f"DROP FUNCTION private.{function}")

def drop_select_all_keys_from_schema_public_functions():
    functions = [
        "select_all_theory_image_keys",
        "select_all_theory_audio_keys",
        "select_all_practice_image_keys",
        "select_all_practice_audio_keys",
        "select_all_book_keys",]

    for function in functions:
        op.execute(f"DROP FUNCTION public.{function}")

def upgrade() -> None:
    create_select_all_keys_from_schema_private_functions()
    craete_select_all_keys_from_schema_public_functions()
    create_link_updating_functions_schema_private()
    create_link_updating_functions_schema_public()

def downgrade() -> None:
    drop_select_all_keys_from_schema_private_functions()
    drop_select_all_keys_from_schema_public_functions()
    drop_link_updating_functions_schema_private()
    drop_link_updating_functions_schema_public()