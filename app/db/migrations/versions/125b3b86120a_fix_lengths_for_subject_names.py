"""fix lengths for subject names
Revision ID: 125b3b86120a
Revises: d101b634aae2
Create Date: 2021-06-22 10:36:33.612101
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '125b3b86120a'
down_revision = 'd101b634aae2'
branch_labels = None
depends_on = None

def create_stored_procedures_insert() -> None:
    # grades insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION private.insert_grade(varchar(100), varchar(100), text, text, int)
        RETURNS TABLE (id int, name_en varchar(100), name_ru varchar(100), background text, background_key text, order_number int)
        AS $$
        DECLARE
        inserted_id int;
        BEGIN
        INSERT INTO private.grade (name_en, name_ru, background_key, background, order_number) VALUES ($1, $2, $3, $4, $5) 
        RETURNING private.grade.id INTO inserted_id;
        RETURN QUERY (SELECT * FROM private.grade WHERE private.grade.id = inserted_id);
        END $$ LANGUAGE plpgsql;
    """)

    # subject insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION private.insert_subject(int, varchar(100), varchar(100), text, text, int)
        RETURNS TABLE (id int, fk int, name_en varchar(100), name_ru varchar(100), background text, background_key text, order_number int)
        AS $$
        DECLARE
        inserted_id int;
        BEGIN
        INSERT INTO private.subject (fk, name_en, name_ru, background_key, background, order_number) VALUES ($1, $2, $3, $4, $5, $6) RETURNING private.subject.id INTO inserted_id;
        RETURN QUERY (SELECT * FROM private.subject WHERE private.subject.id = inserted_id);
        END $$ LANGUAGE plpgsql;
    """)

    # branch insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION private.insert_branch(int, varchar(100), varchar(100), text, text, int)
        RETURNS TABLE (id int, fk int, name_en varchar(100), name_ru varchar(100), background text, background_key text, order_number int)
        AS $$
        DECLARE
        inserted_id int;
        BEGIN
        INSERT INTO private.branch (fk, name_en, name_ru, background_key, background, order_number) VALUES ($1, $2, $3, $4, $5, $6) RETURNING private.branch.id INTO inserted_id;
        RETURN QUERY (SELECT * FROM private.branch WHERE private.branch.id = inserted_id);
        END $$ LANGUAGE plpgsql;
    """)

    # lecture insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION private.insert_lecture(int, varchar(100), varchar(100), text, text, text, int)
        RETURNS TABLE (id int, fk int, name_en varchar(100), name_ru varchar(100), description text, background text, background_key text, order_number int)
        AS $$
        DECLARE
        inserted_id int;
        BEGIN
        INSERT INTO private.lecture (fk, name_en, name_ru, description, background_key, background, order_number) VALUES ($1, $2, $3, $4, $5, $6, $7) RETURNING private.lecture.id INTO inserted_id;
        RETURN QUERY (SELECT * FROM private.lecture WHERE private.lecture.id = inserted_id);
        END $$ LANGUAGE plpgsql;
    """)

    # video insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION private.insert_video(int, varchar(100), text, text, text)
        RETURNS TABLE (id int, url text, name_ru varchar(100), description text, key text)
        AS $$
        DECLARE
        inserted_id int;
        BEGIN
        INSERT INTO private.video (fk, name_ru, description, key, url) VALUES ($1, $2, $3, $4, $5) RETURNING private.video.fk INTO inserted_id;
        RETURN QUERY (SELECT * FROM private.video WHERE private.video.fk = inserted_id);
        END $$ LANGUAGE plpgsql;
    """)

    # book insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION private.insert_book(int, varchar(100), text, text, text)
        RETURNS TABLE (id int, url text, name_ru varchar(100), description text, key text)
        AS $$
        DECLARE
        inserted_id int;
        BEGIN
        INSERT INTO private.book (fk, name_ru, description, key, url) VALUES ($1, $2, $3, $4, $5) RETURNING private.book.fk INTO inserted_id;
        RETURN QUERY (SELECT * FROM private.book WHERE private.book.fk = inserted_id);
        END $$ LANGUAGE plpgsql;
    """)

    # game insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION private.insert_game(int, varchar(100), text, text)
        RETURNS TABLE (id int, url text, name_ru varchar(100), description text)
        AS $$
        DECLARE
        inserted_id int;
        BEGIN
        INSERT INTO private.game (fk, name_ru, description, url) VALUES ($1, $2, $3, $4) RETURNING private.game.fk INTO inserted_id;
        RETURN QUERY (SELECT * FROM private.game WHERE private.game.fk = inserted_id);
        END $$ LANGUAGE plpgsql;
    """)

    # theory insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION private.insert_theory(int, varchar(100), text, text)
        RETURNS TABLE (id int, name_ru varchar(100), description text, key text)
        AS $$
        DECLARE
        inserted_id int;
        BEGIN
        INSERT INTO private.theory (fk, name_ru, description, key) VALUES ($1, $2, $3, $4) RETURNING private.theory.fk INTO inserted_id;
        RETURN QUERY (SELECT * FROM private.theory WHERE private.theory.fk = inserted_id);
        END $$ LANGUAGE plpgsql;
    """)
    # theory images insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION private.insert_theory_image(int[], int[], text[], text[])
        RETURNS TABLE ("order" int, url text, key text)
        AS $$
        BEGIN
        INSERT INTO private.theory_image (fk, "order", url, key)
        SELECT unnest($1), unnest($2), unnest($3), unnest($4);
        RETURN QUERY (SELECT private.theory_image."order", private.theory_image.url, private.theory_image.key FROM private.theory_image WHERE private.theory_image.fk = $1[1]);
        END $$ LANGUAGE plpgsql;
    """)
    # theory audio insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION private.insert_theory_audio(int[], int[], text[], text[])
        RETURNS TABLE ("order" int, url text, key text)
        AS $$
        BEGIN
        INSERT INTO private.theory_audio (fk, "order", url, key)
        SELECT unnest($1), unnest($2), unnest($3), unnest($4);
        RETURN QUERY (SELECT private.theory_audio."order", private.theory_audio.url, private.theory_audio.key FROM private.theory_audio WHERE private.theory_audio.fk = $1[1]);
        END $$ LANGUAGE plpgsql;
    """)

    # practice insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION private.insert_practice(int, varchar(100), text, text)
        RETURNS TABLE (id int, name_ru varchar(100), description text, key text)
        AS $$
        DECLARE
        inserted_id int;
        BEGIN
        INSERT INTO private.practice (fk, name_ru, description, key) VALUES ($1, $2, $3, $4) RETURNING private.practice.fk INTO inserted_id;
        RETURN QUERY (SELECT * FROM private.practice WHERE private.practice.fk = inserted_id);
        END $$ LANGUAGE plpgsql;
    """)
    # practice images insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION private.insert_practice_image(int[], int[], text[], text[])
        RETURNS TABLE ("order" int, url text, key text)
        AS $$
        BEGIN
        INSERT INTO private.practice_image (fk, "order", url, key)
        SELECT unnest($1), unnest($2), unnest($3), unnest($4);
        RETURN QUERY (SELECT private.practice_image."order", private.practice_image.url, private.practice_image.key FROM private.practice_image WHERE private.practice_image.fk = $1[1]);
        END $$ LANGUAGE plpgsql;
    """)
    # practice audio insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION private.insert_practice_audio(int[], int[], text[], text[])
        RETURNS TABLE ("order" int, url text, key text)
        AS $$
        BEGIN
        INSERT INTO private.practice_audio (fk, "order", url, key)
        SELECT unnest($1), unnest($2), unnest($3), unnest($4);
        RETURN QUERY (SELECT private.practice_audio."order", private.practice_audio.url, private.practice_audio.key FROM private.practice_audio WHERE private.practice_audio.fk = $1[1]);
        END $$ LANGUAGE plpgsql;
    """)

def create_stored_procedures_delete() -> None:
    # grades delete function
    op.execute("""
    CREATE OR REPLACE FUNCTION private.delete_grade_by_id(int)
        RETURNS text
        AS $$
        DECLARE key text;
        BEGIN
        DELETE FROM private.grade WHERE private.grade.id = $1 RETURNING background_key INTO key;
        RETURN key;
        END $$ LANGUAGE plpgsql;
    """)
    # subject delete function
    op.execute("""
    CREATE OR REPLACE FUNCTION private.delete_subject_by_id(int)
        RETURNS text
        AS $$
        DECLARE key text;
        BEGIN
        DELETE FROM private.subject WHERE private.subject.id = $1 RETURNING background_key INTO key;
        RETURN key;
        END $$ LANGUAGE plpgsql;
    """)
    # branch delete function
    op.execute("""
    CREATE OR REPLACE FUNCTION private.delete_branch_by_id(int)
        RETURNS text
        AS $$
        DECLARE key text;
        BEGIN
        DELETE FROM private.branch WHERE private.branch.id = $1 RETURNING background_key INTO key;
        RETURN key;
        END $$ LANGUAGE plpgsql;
    """)
    # lecture delete function
    op.execute("""
    CREATE OR REPLACE FUNCTION private.delete_lecture_by_id(int)
        RETURNS text
        AS $$
        DECLARE key text;
        BEGIN
        DELETE FROM private.lecture WHERE private.lecture.id = $1 RETURNING background_key INTO key;
        RETURN key;
        END $$ LANGUAGE plpgsql;
    """)
    # theory delete function
    op.execute("""
    CREATE OR REPLACE FUNCTION private.delete_theory_by_id(int)
        RETURNS text
        AS $$
        DECLARE key text;
        BEGIN
        DELETE FROM private.theory WHERE private.theory.fk = $1 RETURNING private.theory.key INTO key;
        RETURN key;
        END $$ LANGUAGE plpgsql;
    """)
    # practice delete function
    op.execute("""
    CREATE OR REPLACE FUNCTION private.delete_practice_by_id(int)
        RETURNS text
        AS $$
        DECLARE key text;
        BEGIN
        DELETE FROM private.practice WHERE private.practice.fk = $1 RETURNING private.practice.key INTO key;
        RETURN key;
        END $$ LANGUAGE plpgsql;
    """)
    # book delete function
    op.execute("""
    CREATE OR REPLACE FUNCTION private.delete_book_by_id(int)
        RETURNS text
        AS $$
        DECLARE key text;
        BEGIN
        DELETE FROM private.book WHERE private.book.fk = $1 RETURNING private.book.key INTO key;
        RETURN key;
        END $$ LANGUAGE plpgsql;
    """)
    # video delete function
    op.execute("""
    CREATE OR REPLACE FUNCTION private.delete_video_by_id(int)
        RETURNS text
        AS $$
        DECLARE key text;
        BEGIN
        DELETE FROM private.video WHERE private.video.fk = $1 RETURNING private.video.key INTO key;
        RETURN key;
        END $$ LANGUAGE plpgsql;
    """)
    # game delete function
    op.execute("""
    CREATE OR REPLACE FUNCTION private.delete_game_by_id(int)
        RETURNS VOID
        AS $$
        BEGIN
        DELETE FROM private.game WHERE private.game.fk = $1;
        END $$ LANGUAGE plpgsql;
    """)

def create_stored_procedures_select() -> None:
    # grades select functions
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_grades_by_ids(text)
        RETURNS TABLE (id int, name_en varchar(100), name_ru varchar(100), background text, background_key text, order_number int)
        AS $$
        DECLARE 
            ids INT[];
        BEGIN
        ids = string_to_array($1,',');
        RETURN QUERY (SELECT * FROM private.grade WHERE private.grade.id = ANY(ids) ORDER BY private.grade.order_number);
        END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_all_grades()
        RETURNS TABLE (id int, name_en varchar(100), name_ru varchar(100), background text, background_key text, order_number int)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.grade ORDER BY private.grade.order_number);
        END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
     CREATE OR REPLACE FUNCTION private.select_grade_by_name(text)
        RETURNS TABLE (id int, name_en varchar(100), name_ru varchar(100), background text, background_key text, order_number int)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.grade WHERE private.grade.name_en = $1 ORDER BY private.grade.order_number);
        END $$ LANGUAGE plpgsql;
    """)

    # subject select functions
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_subjects_by_ids(text, int)
        RETURNS TABLE (id int, fk int, name_en varchar(100), name_ru varchar(100), background text, background_key text, order_number int)
        AS $$
        DECLARE 
            ids INT[];
        BEGIN
        ids = string_to_array($1,',');
        RETURN QUERY (SELECT * FROM private.subject WHERE private.subject.id = ANY(ids) AND private.subject.fk = $2 ORDER BY private.subject.order_number);
        END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_all_subjects(int)
        RETURNS TABLE (id int, fk int, name_en varchar(100), name_ru varchar(100), background text, background_key text, order_number int)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.subject WHERE private.subject.fk = $1 ORDER BY private.subject.order_number);
        END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_subject_by_name(text, int)
        RETURNS TABLE (id int, fk int, name_en varchar(100), name_ru varchar(100), background text, background_key text, order_number int)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.subject WHERE private.subject.name_en = $1 AND private.subject.fk = $2 ORDER BY private.subject.order_number);
        END $$ LANGUAGE plpgsql;
    """)

    # branch select functions
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_all_branches(int)
        RETURNS TABLE (id int, fk int, name_en varchar(100), name_ru varchar(100), background text, background_key text, order_number int)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.branch WHERE private.branch.fk = $1 ORDER BY private.branch.order_number);
        END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_branch_by_name(text, int)
        RETURNS TABLE (id int, fk int, name_en varchar(100), name_ru varchar(100), background text, background_key text, order_number int)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.branch WHERE private.branch.name_en = $1 AND private.branch.fk = $2 ORDER BY private.branch.order_number);
        END $$ LANGUAGE plpgsql;
    """)

    # lecture select function
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_all_lectures(int)
        RETURNS TABLE (id int, fk int, name_en varchar(100), name_ru varchar(100), description text, background text, background_key text, order_number int)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.lecture WHERE private.lecture.fk = $1 ORDER BY private.lecture.order_number);
        END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_lecture_by_name(text, int)
        RETURNS TABLE (id int, fk int, name_en varchar(100), name_ru varchar(100), description text, background text, background_key text, order_number int)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.lecture WHERE private.lecture.name_en = $1 AND private.lecture.fk = $2 ORDER BY private.lecture.order_number);
        END $$ LANGUAGE plpgsql;
    """)

    # theory
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_theory(int)
        RETURNS TABLE (id int, name_ru varchar(100), description text, key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.theory WHERE private.theory.fk = $1);
        END $$ LANGUAGE plpgsql;
    """)
    # thoery images
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_theory_image(int)
        RETURNS TABLE (url text, "order" int, key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT private.theory_image.url, private.theory_image."order", private.theory_image.key FROM private.theory_image WHERE private.theory_image.fk = $1);
        END $$ LANGUAGE plpgsql;
    """)
    # theory audio
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_theory_audio(int)
        RETURNS TABLE (url text, "order" int, key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT private.theory_audio.url, private.theory_audio."order", private.theory_audio.key FROM private.theory_audio WHERE private.theory_audio.fk = $1);
        END $$ LANGUAGE plpgsql;
    """)
    
    # practice
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_practice(int)
        RETURNS TABLE (id int, name_ru varchar(100), description text, key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.practice WHERE private.practice.fk = $1);
        END $$ LANGUAGE plpgsql;
    """)
    # practice images
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_practice_image(int)
        RETURNS TABLE (url text, "order" int, key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT private.practice_image.url, private.practice_image."order", private.practice_image.key FROM private.practice_image WHERE private.practice_image.fk = $1);
        END $$ LANGUAGE plpgsql;
    """)
    # practice audio
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_practice_audio(int)
        RETURNS TABLE (url text, "order" int, key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT private.practice_audio.url, private.practice_audio."order", private.practice_audio.key FROM private.practice_audio WHERE private.practice_audio.fk = $1);
        END $$ LANGUAGE plpgsql;
    """)

    # select material function
    # NOTE: You can use this function for getting all material data except images and audio
    # for theory and practice IN CASE that you are sure there will be all material in every moment
    # otherwise use separate functions for getting data
    # this function is to be used with MaterialBulk model
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_material(int)
        RETURNS TABLE (video_url text, video_name_ru varchar(100), video_description text, video_key text,
        game_url text, game_name_ru varchar(100), game_description text, theory_name_ru varchar(100), theory_description text, theory_key text,
        practice_name_ru varchar(100), practice_description text, practice_key text, book_url text, book_name_ru varchar(100), book_description text, book_key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT video.url AS video_url, video.name_ru AS video_name_ru, video.description AS video_description, video.key AS video_key,
        game.url AS game_url, game.name_ru AS game_name_ru, game.description AS game_description,
        theory.name_ru AS theory_name_ru, theory.description AS theory_description, theory.key AS theory_key,
        practice.name_ru AS practice_name_ru, practice.description AS practice_description, practice.key AS theory_key,
        book.url AS book_url, book.name_ru AS book_name_ru, book.description AS book_description, book.key AS book_key 
        FROM private.select_video($1) video INNER JOIN private.select_game($1) game ON video.id = game.id
        INNER JOIN private.select_book($1) book ON video.id = book.id INNER JOIN private.select_theory($1) theory
        ON video.id = theory.id INNER JOIN private.select_practice($1) practice ON video.id = practice.id);
        END $$ LANGUAGE plpgsql;  
    """)

    # video
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_video(int)
        RETURNS TABLE (id int, url text, name_ru varchar(100), description text, key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.video WHERE private.video.fk = $1);
        END $$ LANGUAGE plpgsql;
    """)
    
    # book
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_book(int)
        RETURNS TABLE (id int, url text, name_ru varchar(100), description text, key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.book WHERE private.book.fk = $1);
        END $$ LANGUAGE plpgsql;
    """)

    # game
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_game(int)
        RETURNS TABLE (id int, url text, name_ru varchar(100), description text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.game WHERE private.game.fk = $1);
        END $$ LANGUAGE plpgsql;
    """)


def drop_stored_procedures() -> None:
    procedure_list = [
    "select_all_grades",
    "select_grades_by_ids",
    "select_all_subjects(int)",
    "select_theory",
    "select_grade_by_name",
    "select_subjects_by_ids",
    "select_subject_by_name",
    "select_all_branches(int)",
    "select_branch_by_name",
    "select_all_lectures(int)",
    "select_theory_image",
    "select_material",
    "select_lecture_by_name",
    "select_theory_audio",
    "select_video",
    "select_book",
    "select_game",
    "select_practice",
    "select_practice_image",
    "select_practice_audio",
    "insert_grade",
    "insert_game",
    "insert_book",
    "insert_video",
    "insert_theory",
    "insert_theory_image",
    "insert_theory_audio",
    "insert_subject",
    "insert_branch",
    "insert_lecture",
    "insert_practice",
    "insert_practice_image",
    "insert_practice_audio",
    "delete_book_by_id",
    "delete_branch_by_id",
    "delete_game_by_id",
    "delete_grade_by_id",
    "delete_lecture_by_id",
    "delete_practice_by_id",
    "delete_subject_by_id",
    "delete_theory_by_id",
    "delete_video_by_id",
    "update_grade",
    "update_subject",
    "update_branch",
    "update_lecture",
    ]

    for procedure in procedure_list:
        op.execute(f"DROP FUNCTION private.{procedure}")

def update_private_tables() -> None:
    # grades table
    op.execute("ALTER TABLE private.grade ALTER COLUMN name_en TYPE VARCHAR(100), ALTER COLUMN name_ru TYPE VARCHAR(100)")
    op.execute("ALTER TABLE private.grade ADD COLUMN order_number INTEGER NOT NULL DEFAULT 0")

    # subjects table
    op.execute("ALTER TABLE private.subject ALTER COLUMN name_en TYPE VARCHAR(100), ALTER COLUMN name_ru TYPE VARCHAR(100)")
    op.execute("ALTER TABLE private.subject ADD COLUMN order_number INTEGER NOT NULL DEFAULT 0")

    # branches table
    op.execute("ALTER TABLE private.branch ALTER COLUMN name_en TYPE VARCHAR(100), ALTER COLUMN name_ru TYPE VARCHAR(100)")
    op.execute("ALTER TABLE private.branch ADD COLUMN order_number INTEGER NOT NULL DEFAULT 0")

    # lectures table
    op.execute("ALTER TABLE private.lecture ALTER COLUMN name_en TYPE VARCHAR(100), ALTER COLUMN name_ru TYPE VARCHAR(100)")
    op.execute("ALTER TABLE private.lecture ADD COLUMN order_number INTEGER NOT NULL DEFAULT 0")

    # material tables
    # video
    op.execute("ALTER TABLE private.video ALTER COLUMN name_ru TYPE VARCHAR(100)")

    # game
    op.execute("ALTER TABLE private.game ALTER COLUMN name_ru TYPE VARCHAR(100)")

    # book
    op.execute("ALTER TABLE private.book ALTER COLUMN name_ru TYPE VARCHAR(100)")

    # theory
    op.execute("ALTER TABLE private.theory ALTER COLUMN name_ru TYPE VARCHAR(100)")
    
    # practice
    op.execute("ALTER TABLE private.practice ALTER COLUMN name_ru TYPE VARCHAR(100)")

    # drop redundant table
    op.execute("DROP TABLE private.timestamp CASCADE")


def remove_order_number() -> None:
    op.execute("ALTER TABLE private.grade DROP COLUMN order_number")
    op.execute("ALTER TABLE private.subject DROP COLUMN order_number")
    op.execute("ALTER TABLE private.branch DROP COLUMN order_number")
    op.execute("ALTER TABLE private.lecture DROP COLUMN order_number")

def remove_order_number_from_functions() -> None:
    # ###
    # SELECT
    # ###
    # grades select functions
    op.execute("DROP FUNCTION private.select_grades_by_ids(text)")
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_grades_by_ids(text)
        RETURNS TABLE (id int, name_en varchar(100), name_ru varchar(100), background text, background_key text)
        AS $$
        DECLARE 
            ids INT[];
        BEGIN
        ids = string_to_array($1,',');
        RETURN QUERY (SELECT * FROM private.grade WHERE private.grade.id = ANY(ids));
        END $$ LANGUAGE plpgsql;
    """)

    op.execute("DROP FUNCTION private.select_all_grades()")
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_all_grades()
        RETURNS TABLE (id int, name_en varchar(100), name_ru varchar(100), background text, background_key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.grade);
        END $$ LANGUAGE plpgsql;
    """)

    op.execute("DROP FUNCTION private.select_grade_by_name(text)")
    op.execute("""
     CREATE OR REPLACE FUNCTION private.select_grade_by_name(text)
        RETURNS TABLE (id int, name_en varchar(100), name_ru varchar(100), background text, background_key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.grade WHERE private.grade.name_en = $1);
        END $$ LANGUAGE plpgsql;
    """)

    # subject select functions
    op.execute("DROP FUNCTION private.select_subjects_by_ids(text, int)")
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_subjects_by_ids(text, int)
        RETURNS TABLE (id int, fk int, name_en varchar(100), name_ru varchar(100), background text, background_key text)
        AS $$
        DECLARE 
            ids INT[];
        BEGIN
        ids = string_to_array($1,',');
        RETURN QUERY (SELECT * FROM private.subject WHERE private.subject.id = ANY(ids) AND private.subject.fk = $2);
        END $$ LANGUAGE plpgsql;
    """)

    op.execute("DROP FUNCTION private.select_all_subjects(int)")
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_all_subjects(int)
        RETURNS TABLE (id int, fk int, name_en varchar(100), name_ru varchar(100), background text, background_key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.subject WHERE private.subject.fk = $1);
        END $$ LANGUAGE plpgsql;
    """)

    op.execute("DROP FUNCTION private.select_subject_by_name(text, int)")
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_subject_by_name(text, int)
        RETURNS TABLE (id int, fk int, name_en varchar(100), name_ru varchar(100), background text, background_key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.subject WHERE private.subject.name_en = $1 AND private.subject.fk = $2);
        END $$ LANGUAGE plpgsql;
    """)

    # branch select functions
    op.execute("DROP FUNCTION private.select_all_branches(int)")
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_all_branches(int)
        RETURNS TABLE (id int, fk int, name_en varchar(100), name_ru varchar(100), background text, background_key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.branch WHERE private.branch.fk = $1);
        END $$ LANGUAGE plpgsql;
    """)

    op.execute("DROP FUNCTION private.select_branch_by_name(text, int)")
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_branch_by_name(text, int)
        RETURNS TABLE (id int, fk int, name_en varchar(100), name_ru varchar(100), background text, background_key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.branch WHERE private.branch.name_en = $1 AND private.branch.fk = $2);
        END $$ LANGUAGE plpgsql;
    """)

    # lecture select function
    op.execute("DROP FUNCTION private.select_all_lectures(int)")
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_all_lectures(int)
        RETURNS TABLE (id int, fk int, name_en varchar(100), name_ru varchar(100), description text, background text, background_key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.lecture WHERE private.lecture.fk = $1);
        END $$ LANGUAGE plpgsql;
    """)

    op.execute("DROP FUNCTION private.select_lecture_by_name(text, int)")
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_lecture_by_name(text, int)
        RETURNS TABLE (id int, fk int, name_en varchar(100), name_ru varchar(100), description text, background text, background_key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.lecture WHERE private.lecture.name_en = $1 AND private.lecture.fk = $2);
        END $$ LANGUAGE plpgsql;
    """)


    # ###
    # INSERT
    # ###
    # grades insert function
    op.execute("DROP FUNCTION private.insert_grade")
    op.execute("""
    CREATE OR REPLACE FUNCTION private.insert_grade(varchar(100), varchar(100), text, text)
        RETURNS TABLE (id int, name_en varchar(100), name_ru varchar(100), background text, background_key text)
        AS $$
        DECLARE
        inserted_id int;
        BEGIN
        INSERT INTO private.grade (name_en, name_ru, background_key, background) VALUES ($1, $2, $3, $4) 
        RETURNING private.grade.id INTO inserted_id;
        RETURN QUERY (SELECT * FROM private.grade WHERE private.grade.id = inserted_id);
        END $$ LANGUAGE plpgsql;
    """)

    # subject insert function
    op.execute("DROP FUNCTION private.insert_subject")
    op.execute("""
    CREATE OR REPLACE FUNCTION private.insert_subject(int, varchar(100), varchar(100), text, text)
        RETURNS TABLE (id int, fk int, name_en varchar(100), name_ru varchar(100), background text, background_key text)
        AS $$
        DECLARE
        inserted_id int;
        BEGIN
        INSERT INTO private.subject (fk, name_en, name_ru, background_key, background) VALUES ($1, $2, $3, $4, $5) RETURNING private.subject.id INTO inserted_id;
        RETURN QUERY (SELECT * FROM private.subject WHERE private.subject.id = inserted_id);
        END $$ LANGUAGE plpgsql;
    """)

    # branch insert function
    op.execute("DROP FUNCTION private.insert_branch")
    op.execute("""
    CREATE OR REPLACE FUNCTION private.insert_branch(int, varchar(100), varchar(100), text, text)
        RETURNS TABLE (id int, fk int, name_en varchar(100), name_ru varchar(100), background text, background_key text)
        AS $$
        DECLARE
        inserted_id int;
        BEGIN
        INSERT INTO private.branch (fk, name_en, name_ru, background_key, background) VALUES ($1, $2, $3, $4, $5) RETURNING private.branch.id INTO inserted_id;
        RETURN QUERY (SELECT * FROM private.branch WHERE private.branch.id = inserted_id);
        END $$ LANGUAGE plpgsql;
    """)

    # lecture insert function
    op.execute("DROP FUNCTION private.insert_lecture")
    op.execute("""
    CREATE OR REPLACE FUNCTION private.insert_lecture(int, varchar(100), varchar(100), text, text, text)
        RETURNS TABLE (id int, fk int, name_en varchar(100), name_ru varchar(100), description text, background text, background_key text)
        AS $$
        DECLARE
        inserted_id int;
        BEGIN
        INSERT INTO private.lecture (fk, name_en, name_ru, description, background_key, background) VALUES ($1, $2, $3, $4, $5, $6) RETURNING private.lecture.id INTO inserted_id;
        RETURN QUERY (SELECT * FROM private.lecture WHERE private.lecture.id = inserted_id);
        END $$ LANGUAGE plpgsql;
    """)

    # create dummy table timestamp for us to delete later in upgrade
    op.create_table(
        "timestamp", 
        sa.Column("id", sa.Integer, primary_key=True),
        schema="private"
    )

def create_stored_procedures_update() -> None:
    # update grade functions
    op.execute("""
    CREATE OR REPLACE FUNCTION private.update_grade(int, varchar(20), text, text, int)
        RETURNS TABLE (id int, name_en varchar(20), name_ru varchar(20), background text, background_key text, order_number int)
        AS $$
        BEGIN
        UPDATE private.grade SET 
        name_ru = COALESCE($2, private.grade.name_ru),
        background = COALESCE($3, private.grade.background),
        background_key = COALESCE($4, private.grade.background_key),
        order_number = COALESCE($5, private.grade.order_number)
        WHERE private.grade.id = $1;
        RETURN QUERY (SELECT * FROM private.grade WHERE private.grade.id = $1);
        END $$ LANGUAGE plpgsql;
    """)

    # subject
    op.execute("""
    CREATE OR REPLACE FUNCTION private.update_subject(int, varchar(20), text, text, int)
        RETURNS TABLE (id int, fk int, name_en varchar(20), name_ru varchar(20), background text, background_key text, order_number int)
        AS $$
        BEGIN
        UPDATE private.subject SET 
        name_ru = COALESCE($2, private.subject.name_ru),
        background = COALESCE($3, private.subject.background),
        background_key = COALESCE($4, private.subject.background_key),
        order_number = COALESCE($5, private.subject.order_number)
        WHERE private.subject.id = $1;
        RETURN QUERY (SELECT * FROM private.subject WHERE private.subject.id = $1);
        END $$ LANGUAGE plpgsql;
    """)

    # branch
    op.execute("""
    CREATE OR REPLACE FUNCTION private.update_branch(int, varchar(20), text, text, int)
        RETURNS TABLE (id int, fk int, name_en varchar(20), name_ru varchar(20), background text, background_key text, order_number int)
        AS $$
        BEGIN
        UPDATE private.branch SET 
        name_ru = COALESCE($2, private.branch.name_ru),
        background = COALESCE($3, private.branch.background),
        background_key = COALESCE($4, private.branch.background_key),
        order_number = COALESCE($5, private.branch.order_number)
        WHERE private.branch.id = $1;
        RETURN QUERY (SELECT * FROM private.branch WHERE private.branch.id = $1);
        END $$ LANGUAGE plpgsql;
    """)
    
    # lecture
    op.execute("""
    CREATE OR REPLACE FUNCTION private.update_lecture(int, varchar(20), text, text, text, int)
        RETURNS TABLE (id int, fk int, name_en varchar(20), name_ru varchar(20), description text, background text, background_key text, order_number int)
        AS $$
        BEGIN
        UPDATE private.lecture SET 
        name_ru = COALESCE($2, private.lecture.name_ru),
        description = COALESCE($3, private.lecture.description),
        background = COALESCE($4, private.lecture.background),
        background_key = COALESCE($5, private.lecture.background_key),
        order_number = COALESCE($6, private.lecture.order_number)
        WHERE private.lecture.id = $1;
        RETURN QUERY (SELECT * FROM private.lecture WHERE private.lecture.id = $1);
        END $$ LANGUAGE plpgsql;
    """)


# REMOVE UNIQUE CONSTRAINT FROM ABOUT_US -> OUR_TEAM ON order_number
def remove_unique_constraint_our_team() -> None:
    op.execute('ALTER TABLE about.our_team ADD COLUMN id SERIAL PRIMARY KEY, DROP CONSTRAINT IF EXISTS our_team_order_key')

    op.execute("DROP FUNCTION about.insert_our_team")
    # create team
    op.execute('''
    CREATE OR REPLACE FUNCTION about.insert_our_team(i_order int, i_name text, i_role text, i_profession text, i_description text, i_photo_key text, i_photo_link text)
        RETURNS TABLE ("order" int, name text, role text, profession text, description text, photo_key text, photo_link text, id int)
        AS $$
        DECLARE 
            inserted_id int;
        BEGIN 
        INSERT INTO about.our_team ("order", name, role, profession, description, photo_key, photo_link)
        VALUES (i_order, i_name, i_role,i_profession, i_description, i_photo_key, i_photo_link) RETURNING about.our_team."order" INTO inserted_id;
        RETURN QUERY (SELECT * FROM about.our_team WHERE about.our_team.id = inserted_id);
        END $$ LANGUAGE plpgsql;
    ''')

    op.execute("DROP FUNCTION about.select_all_team_members()")
    # select all team members
    op.execute('''
    CREATE OR REPLACE FUNCTION about.select_all_team_members()
        RETURNS TABLE ("order" int, name text, role text, profession text, description text, photo_key text, photo_link text, id int)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM about.our_team ORDER BY "order");
        END $$ LANGUAGE plpgsql;
    ''')

    op.execute("DROP FUNCTION about.update_team_member(integer,integer,text,text,text,text,text,text)")
    # update team member
    op.execute('''
    CREATE OR REPLACE FUNCTION about.update_team_member(id_ int, i_order int, i_name text, i_role text, i_profession text, i_photo_key text, i_photo_link text,  i_description text)
        RETURNS TABLE ("order" int, name text, role text, profession text, description text, photo_key text, photo_link text, id int)
        AS $$
        BEGIN
        UPDATE about.our_team SET
            "order" = COALESCE(i_order, about.our_team.order),
            name = COALESCE(i_name, about.our_team.name),
            role = COALESCE(i_role, about.our_team.role),
            profession = COALESCE(i_profession, about.our_team.profession), 
            description = COALESCE(i_description, about.our_team.description),
            photo_key = COALESCE(i_photo_key, about.our_team.photo_key),
            photo_link = COALESCE(i_photo_link, about.our_team.photo_link)
        WHERE about.our_team.id = id_;
        RETURN QUERY (SELECT * FROM about.our_team WHERE about.our_team.id = id_);
        END $$ LANGUAGE plpgsql;
    ''')

    op.execute("DROP FUNCTION about.delete_team_member")
    # delete team member
    op.execute('''
    CREATE OR REPLACE FUNCTION about.delete_team_member(id_ int)
        RETURNS VOID 
        AS $$
        BEGIN 
        DELETE FROM about.our_team WHERE id = id_;
        END $$ LANGUAGE plpgsql;
    ''')

def add_unique_constraint_our_team() -> None:
    op.execute('ALTER TABLE about.our_team DROP COLUMN id')



# FIX PAYMENT PROCESS 
def fix_payment_process() -> None:
    # check if user has already submited subscription request for given offer
    # if he did, return old token instead of creating new payment request
    op.execute("DROP FUNCTION subscriptions.check_subscription_pending(int, int, int)")
    op.execute("""
    CREATE OR REPLACE FUNCTION subscriptions.check_subscription_pending(i_user_fk int, i_offer_fk int, i_level int)
    RETURNS TEXT
    AS $$
    DECLARE token TEXT;
    BEGIN
        SELECT payment_id INTO token FROM subscriptions.pending_subscriptions WHERE user_fk = i_user_fk AND offer_fk = i_offer_fk AND level = i_level::boolean;
        RETURN token;
    END $$ LANGUAGE plpgsql;
    """)


def upgrade() -> None:
    drop_stored_procedures()
    update_private_tables()
    create_stored_procedures_insert()
    create_stored_procedures_select()
    create_stored_procedures_delete()
    create_stored_procedures_update()
    remove_unique_constraint_our_team()
    fix_payment_process()

def downgrade() -> None:
    remove_order_number()
    remove_order_number_from_functions()
    add_unique_constraint_our_team()