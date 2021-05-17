"""Initial migration
Revision ID: 1be6fb9d9d8a
Revises: 
Create Date: 2021-03-21 13:33:39.373009
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '1be6fb9d9d8a'
down_revision = None
branch_labels = None
depends_on = None

def create_stored_procedures_insert() -> None:
    # grades insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION private.insert_grade(varchar(20), varchar(20), text, text)
        RETURNS TABLE (id int, name_en varchar(20), name_ru varchar(20), background text, background_key text)
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
    op.execute("""
    CREATE OR REPLACE FUNCTION private.insert_subject(int, varchar(20), varchar(20), text, text)
        RETURNS TABLE (id int, fk int, name_en varchar(20), name_ru varchar(20), background text, background_key text)
        AS $$
        DECLARE
        inserted_id int;
        BEGIN
        INSERT INTO private.subject (fk, name_en, name_ru, background_key, background) VALUES ($1, $2, $3, $4, $5) RETURNING private.subject.id INTO inserted_id;
        RETURN QUERY (SELECT * FROM private.subject WHERE private.subject.id = inserted_id);
        END $$ LANGUAGE plpgsql;
    """)

    # branch insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION private.insert_branch(int, varchar(20), varchar(20), text, text)
        RETURNS TABLE (id int, fk int, name_en varchar(20), name_ru varchar(20), background text, background_key text)
        AS $$
        DECLARE
        inserted_id int;
        BEGIN
        INSERT INTO private.branch (fk, name_en, name_ru, background_key, background) VALUES ($1, $2, $3, $4, $5) RETURNING private.branch.id INTO inserted_id;
        RETURN QUERY (SELECT * FROM private.branch WHERE private.branch.id = inserted_id);
        END $$ LANGUAGE plpgsql;
    """)

    # lecture insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION private.insert_lecture(int, varchar(20), varchar(20), text, text, text)
        RETURNS TABLE (id int, fk int, name_en varchar(20), name_ru varchar(20), description text, background text, background_key text)
        AS $$
        DECLARE
        inserted_id int;
        BEGIN
        INSERT INTO private.lecture (fk, name_en, name_ru, description, background_key, background) VALUES ($1, $2, $3, $4, $5, $6) RETURNING private.lecture.id INTO inserted_id;
        RETURN QUERY (SELECT * FROM private.lecture WHERE private.lecture.id = inserted_id);
        END $$ LANGUAGE plpgsql;
    """)

    # video insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION private.insert_video(int, varchar(20), text, text, text)
        RETURNS TABLE (id int, url text, name_ru varchar(20), description text, key text)
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
    CREATE OR REPLACE FUNCTION private.insert_book(int, varchar(20), text, text, text)
        RETURNS TABLE (id int, url text, name_ru varchar(20), description text, key text)
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
    CREATE OR REPLACE FUNCTION private.insert_game(int, varchar(20), text, text)
        RETURNS TABLE (id int, url text, name_ru varchar(20), description text)
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
    CREATE OR REPLACE FUNCTION private.insert_theory(int, varchar(20), text, text)
        RETURNS TABLE (id int, name_ru varchar(20), description text, key text)
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
    CREATE OR REPLACE FUNCTION private.insert_practice(int, varchar(20), text, text)
        RETURNS TABLE (id int, name_ru varchar(20), description text, key text)
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
        RETURNS TABLE (id int, name_en varchar(20), name_ru varchar(20), background text, background_key text)
        AS $$
        DECLARE 
            ids INT[];
        BEGIN
        ids = string_to_array($1,',');
        RETURN QUERY (SELECT * FROM private.grade WHERE private.grade.id = ANY(ids));
        END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_all_grades()
        RETURNS TABLE (id int, name_en varchar(20), name_ru varchar(20), background text, background_key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.grade);
        END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
     CREATE OR REPLACE FUNCTION private.select_grade_by_name(text)
        RETURNS TABLE (id int, name_en varchar(20), name_ru varchar(20), background text, background_key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.grade WHERE private.grade.name_en = $1);
        END $$ LANGUAGE plpgsql;
    """)

    # subject select functions
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_subjects_by_ids(text, int)
        RETURNS TABLE (id int, fk int, name_en varchar(20), name_ru varchar(20), background text, background_key text)
        AS $$
        DECLARE 
            ids INT[];
        BEGIN
        ids = string_to_array($1,',');
        RETURN QUERY (SELECT * FROM private.subject WHERE private.subject.id = ANY(ids) AND private.subject.fk = $2);
        END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_all_subjects(int)
        RETURNS TABLE (id int, fk int, name_en varchar(20), name_ru varchar(20), background text, background_key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.subject WHERE private.subject.fk = $1);
        END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_subject_by_name(text, int)
        RETURNS TABLE (id int, fk int, name_en varchar(20), name_ru varchar(20), background text, background_key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.subject WHERE private.subject.name_en = $1 AND private.subject.fk = $2);
        END $$ LANGUAGE plpgsql;
    """)

    # branch select functions
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_all_branches(int)
        RETURNS TABLE (id int, fk int, name_en varchar(20), name_ru varchar(20), background text, background_key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.branch WHERE private.branch.fk = $1);
        END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_branch_by_name(text, int)
        RETURNS TABLE (id int, fk int, name_en varchar(20), name_ru varchar(20), background text, background_key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.branch WHERE private.branch.name_en = $1 AND private.branch.fk = $2);
        END $$ LANGUAGE plpgsql;
    """)

    # lecture select function
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_all_lectures(int)
        RETURNS TABLE (id int, fk int, name_en varchar(20), name_ru varchar(20), description text, background text, background_key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.lecture WHERE private.lecture.fk = $1);
        END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_lecture_by_name(text, int)
        RETURNS TABLE (id int, fk int, name_en varchar(20), name_ru varchar(20), description text, background text, background_key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.lecture WHERE private.lecture.name_en = $1 AND private.lecture.fk = $2);
        END $$ LANGUAGE plpgsql;
    """)

    # theory
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_theory(int)
        RETURNS TABLE (id int, name_ru varchar(20), description text, key text)
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
        RETURNS TABLE (id int, name_ru varchar(20), description text, key text)
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
        RETURNS TABLE (video_url text, video_name_ru varchar(20), video_description text, video_key text,
        game_url text, game_name_ru varchar(20), game_description text, theory_name_ru varchar(20), theory_description text, theory_key text,
        practice_name_ru varchar(20), practice_description text, practice_key text, book_url text, book_name_ru varchar(20), book_description text, book_key text)
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
        RETURNS TABLE (id int, url text, name_ru varchar(20), description text, key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.video WHERE private.video.fk = $1);
        END $$ LANGUAGE plpgsql;
    """)
    
    # book
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_book(int)
        RETURNS TABLE (id int, url text, name_ru varchar(20), description text, key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.book WHERE private.book.fk = $1);
        END $$ LANGUAGE plpgsql;
    """)

    # game
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_game(int)
        RETURNS TABLE (id int, url text, name_ru varchar(20), description text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.game WHERE private.game.fk = $1);
        END $$ LANGUAGE plpgsql;
    """)


def drop_stored_procedures() -> None:
    procedure_list = [
    "select_all_grades",
    "select_all_grade_keys",
    "select_grades_by_ids",
    "select_all_subjects(int)",
    "select_all_subject_keys",
    "select_theory",
    "select_grade_by_name",
    "select_subjects_by_ids",
    "select_subject_by_name",
    "select_all_branches(int)",
    "select_all_branch_keys",
    "select_branch_by_name",
    "select_all_lectures(int)",
    "select_all_lecture_keys",
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
    "delete_video_by_id",]

    for procedure in procedure_list:
        op.execute(f"DROP FUNCTION private.{procedure}")

def create_private_tables() -> None:
    # grades table
    op.create_table(
        "grade", 
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name_en", sa.String(20), nullable=False),
        sa.Column("name_ru", sa.String(20), nullable=False),
        sa.Column("background", sa.Text, nullable=False),
        sa.Column("background_key", sa.Text, nullable=False),
        sa.UniqueConstraint('name_en'),
        schema="private"
    )

    # subjects table
    op.create_table(
        "subject",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("fk", sa.Integer, nullable=False),
        sa.Column("name_en", sa.String(20), nullable=False),
        sa.Column("name_ru", sa.String(20), nullable=False),
        sa.Column("background", sa.Text, nullable=False),
        sa.Column("background_key", sa.Text, nullable=False),
        sa.ForeignKeyConstraint(['fk'], ['private.grade.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.UniqueConstraint('fk', 'name_en'),
        schema="private"    
    )

    # branches table
    op.create_table(
        "branch",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("fk", sa.Integer, nullable=False),
        sa.Column("name_en", sa.String(20), nullable=False),
        sa.Column("name_ru", sa.String(20), nullable=False),
        sa.Column("background", sa.Text, nullable=False),
        sa.Column("background_key", sa.Text, nullable=False),
        sa.ForeignKeyConstraint(['fk'], ['private.subject.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.UniqueConstraint('fk', 'name_en'),
        schema="private"    
    )

    # lectures table
    op.create_table(
        "lecture",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("fk", sa.Integer, nullable=False),
        sa.Column("name_en", sa.String(20), nullable=False),
        sa.Column("name_ru", sa.String(20), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("background", sa.Text, nullable=False),
        sa.Column("background_key", sa.Text, nullable=False),
        sa.ForeignKeyConstraint(['fk'], ['private.branch.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.UniqueConstraint('fk', 'name_en'),
        schema="private"    
    )

    # material tables
    # video
    op.create_table(
        "video",
        sa.Column("fk", sa.Integer, nullable=False),
        sa.Column("url", sa.Text, nullable=False),
        sa.Column("name_ru", sa.String(20), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("key", sa.Text, nullable=True),
        sa.ForeignKeyConstraint(['fk'], ['private.lecture.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.UniqueConstraint('fk'),
        schema="private"    
    )
    # game
    op.create_table(
        "game",
        sa.Column("fk", sa.Integer, nullable=False),
        sa.Column("url", sa.Text, nullable=False),
        sa.Column("name_ru", sa.String(20), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.ForeignKeyConstraint(['fk'], ['private.lecture.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.UniqueConstraint('fk'),
        schema="private"    
    )
    # book
    op.create_table(
        "book",
        sa.Column("fk", sa.Integer, nullable=False),
        sa.Column("url", sa.Text, nullable=False),
        sa.Column("name_ru", sa.String(20), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("key", sa.Text, nullable=False),
        sa.ForeignKeyConstraint(['fk'], ['private.lecture.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.UniqueConstraint('fk'),
        schema="private"    
    )
    # theory
    op.create_table(
        "theory",
        sa.Column("fk", sa.Integer, nullable=False),
        sa.Column("name_ru", sa.String(20), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("key", sa.Text, nullable=False),
        sa.ForeignKeyConstraint(['fk'], ['private.lecture.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.UniqueConstraint('fk'),
        schema="private"    
    )
    # practice
    op.create_table(
        "practice",
        sa.Column("fk", sa.Integer, nullable=False),
        sa.Column("name_ru", sa.String(20), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("key", sa.Text, nullable=False),
        sa.ForeignKeyConstraint(['fk'], ['private.lecture.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.UniqueConstraint('fk'),
        schema="private"    
    )
    # theory images
    op.create_table(
        "theory_image",
        sa.Column("fk", sa.Integer, nullable=False),
        sa.Column("order", sa.Integer, nullable=False),
        sa.Column("url", sa.Text, nullable=False),
        sa.Column("key", sa.Text, nullable=False),
        sa.ForeignKeyConstraint(['fk'], ['private.theory.fk'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.UniqueConstraint("fk", "order"),
        schema="private"
    )    
    # theory audio
    op.create_table(
        "theory_audio",
        sa.Column("fk", sa.Integer, nullable=False),
        sa.Column("order", sa.Integer, nullable=False),
        sa.Column("url", sa.Text, nullable=False),
        sa.Column("key", sa.Text, nullable=False),
        sa.ForeignKeyConstraint(['fk'], ['private.theory.fk'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.UniqueConstraint("fk", "order"),
        schema="private"
    )    
    # practice images
    op.create_table(
        "practice_image",
        sa.Column("fk", sa.Integer, nullable=False),
        sa.Column("order", sa.Integer, nullable=False),
        sa.Column("url", sa.Text, nullable=False),
        sa.Column("key", sa.Text, nullable=False),
        sa.ForeignKeyConstraint(['fk'], ['private.practice.fk'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.UniqueConstraint("fk", "order"),
        schema="private"
    )    
    # practice audio
    op.create_table(
        "practice_audio",
        sa.Column("fk", sa.Integer, nullable=False),
        sa.Column("order", sa.Integer, nullable=False),
        sa.Column("url", sa.Text, nullable=False),
        sa.Column("key", sa.Text, nullable=False),
        sa.ForeignKeyConstraint(['fk'], ['private.practice.fk'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.UniqueConstraint("fk", "order"),
        schema="private"
    )    
    # timestamp
    op.create_table(
        "timestamp",
        sa.Column("last_update",  sa.TIMESTAMP(timezone=True),server_default=sa.func.now(), nullable=False),
        sa.Column("is_updating", sa.Boolean, nullable=False),
        schema="private",
    )

    op.execute("""
        CREATE OR REPLACE FUNCTION update_timestamp_function()
            RETURNS TRIGGER AS
        $$
        BEGIN
        IF NEW.is_updating = 'f' THEN
            RAISE NOTICE 'SHOULD UPDATE';
            UPDATE private.timestamp
            SET last_update = now();
            RETURN NEW;
        ELSE
            RAISE NOTICE 'SHOULDNT UPDATE';
            RETURN NEW;
        END IF;
        END;
        $$ language 'plpgsql';

    """)

    op.execute("""
        CREATE TRIGGER update_timestamp
        AFTER UPDATE OF is_updating ON private.timestamp 
        FOR EACH ROW
        EXECUTE PROCEDURE update_timestamp_function()
    """)



def drop_private_tables() -> None:
    op.drop_table("theory_image", schema="private")
    op.drop_table("theory_audio", schema="private")
    op.drop_table("practice_image", schema="private")
    op.drop_table("practice_audio", schema="private")
    op.drop_table("practice", schema="private")
    op.drop_table("theory", schema="private")
    op.drop_table("book", schema="private")
    op.drop_table("game", schema="private")
    op.drop_table("video", schema="private")
    op.drop_table("lecture", schema="private")
    op.drop_table("branch", schema="private")
    op.drop_table("subject", schema="private")
    op.drop_table("grade", schema="private")
    op.drop_table('timestamp', schema='private')

def upgrade() -> None:
    create_private_tables()
    create_stored_procedures_insert()
    create_stored_procedures_select()
    create_stored_procedures_delete()

def downgrade() -> None:
    drop_private_tables()
    drop_stored_procedures()