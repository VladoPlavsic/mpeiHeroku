"""Check if content can be created - private
Revision ID: 877c67c2ae29
Revises: 000fc98ce9cf
Create Date: 2021-07-14 10:14:02.431281
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '877c67c2ae29'
down_revision = '000fc98ce9cf'
branch_labels = None
depends_on = None

def create_insert_check_functions() -> None:
    op.execute("""
    CREATE OR REPLACE FUNCTION private.grade_can_be_created(i_name_en VARCHAR(100))
    RETURNS BOOLEAN
    AS $$
    DECLARE 
        yes BOOLEAN;
    BEGIN
        SELECT COUNT(*)::int::bool FROM private.grade WHERE name_en = i_name_en INTO yes;
        yes = NOT yes;
        RETURN yes;
    END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION private.subject_can_be_created(i_fk INT, i_name_en VARCHAR(100))
    RETURNS BOOLEAN
    AS $$
    DECLARE 
        yes BOOLEAN;
        fk_exists BOOLEAN;
    BEGIN
        SELECT COUNT(*)::int::bool FROM private.grade WHERE id = i_fk INTO fk_exists;
        IF fk_exists THEN
            SELECT COUNT(*)::int::bool FROM private.subject WHERE fk = i_fk AND name_en = i_name_en INTO yes;
            yes = NOT yes;
            RETURN yes;
        ELSE
            RETURN 'f';
        END IF;
    END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION private.branch_can_be_created(i_fk INT, i_name_en VARCHAR(100))
    RETURNS BOOLEAN
    AS $$
    DECLARE 
        yes BOOLEAN;
        fk_exists BOOLEAN;
    BEGIN
        SELECT COUNT(*)::int::bool FROM private.subject WHERE id = i_fk INTO fk_exists;
        IF fk_exists THEN
            SELECT COUNT(*)::int::bool FROM private.branch WHERE fk = i_fk AND name_en = i_name_en INTO yes;
            yes = NOT yes;
            RETURN yes;
        ELSE
            RETURN 'f';
        END IF;
    END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION private.lecture_can_be_created(i_fk INT, i_name_en VARCHAR(100))
    RETURNS BOOLEAN
    AS $$
    DECLARE 
        yes BOOLEAN;
        fk_exists BOOLEAN;
    BEGIN
        SELECT COUNT(*)::int::bool FROM private.branch WHERE id = i_fk INTO fk_exists;
        IF fk_exists THEN
            SELECT COUNT(*)::int::bool FROM private.lecture WHERE fk = i_fk AND name_en = i_name_en INTO yes;
            yes = NOT yes;
            RETURN yes;
        ELSE
            RETURN 'f';
        END IF;
    END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION private.video_can_be_created(i_fk INT)
    RETURNS BOOLEAN
    AS $$
    DECLARE 
        yes BOOLEAN;
        fk_exists BOOLEAN;
    BEGIN
        SELECT COUNT(*)::int::bool FROM private.lecture WHERE id = i_fk INTO fk_exists;
        IF fk_exists THEN
            SELECT COUNT(*)::int::bool FROM private.video WHERE fk = i_fk INTO yes;
            yes = NOT yes;
            RETURN yes;
        ELSE
            RETURN 'f';
        END IF;
    END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION private.game_can_be_created(i_fk INT)
    RETURNS BOOLEAN
    AS $$
    DECLARE 
        yes BOOLEAN;
        fk_exists BOOLEAN;
    BEGIN
        SELECT COUNT(*)::int::bool FROM private.lecture WHERE id = i_fk INTO fk_exists;
        IF fk_exists THEN
            SELECT COUNT(*)::int::bool FROM private.game WHERE fk = i_fk INTO yes;
            yes = NOT yes;
            RETURN yes;
        ELSE
            RETURN 'f';
        END IF;
    END $$ LANGUAGE plpgsql;
    """)
    
    op.execute("""
    CREATE OR REPLACE FUNCTION private.book_can_be_created(i_fk INT)
    RETURNS BOOLEAN
    AS $$
    DECLARE 
        yes BOOLEAN;
        fk_exists BOOLEAN;
    BEGIN
        SELECT COUNT(*)::int::bool FROM private.lecture WHERE id = i_fk INTO fk_exists;
        IF fk_exists THEN
            SELECT COUNT(*)::int::bool FROM private.book WHERE fk = i_fk INTO yes;
            yes = NOT yes;
            RETURN yes;
        ELSE
            RETURN 'f';
        END IF;
    END $$ LANGUAGE plpgsql;
    """)
    
    op.execute("""
    CREATE OR REPLACE FUNCTION private.theory_can_be_created(i_fk INT)
    RETURNS BOOLEAN
    AS $$
    DECLARE 
        yes BOOLEAN;
        fk_exists BOOLEAN;
    BEGIN
        SELECT COUNT(*)::int::bool FROM private.lecture WHERE id = i_fk INTO fk_exists;
        IF fk_exists THEN
            SELECT COUNT(*)::int::bool FROM private.theory WHERE fk = i_fk INTO yes;
            yes = NOT yes;
            RETURN yes;
        ELSE
            RETURN 'f';
        END IF;
    END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION private.practice_can_be_created(i_fk INT)
    RETURNS BOOLEAN
    AS $$
    DECLARE 
        yes BOOLEAN;
        fk_exists BOOLEAN;
    BEGIN
        SELECT COUNT(*)::int::bool FROM private.lecture WHERE id = i_fk INTO fk_exists;
        IF fk_exists THEN
            SELECT COUNT(*)::int::bool FROM private.practice WHERE fk = i_fk INTO yes;
            yes = NOT yes;
            RETURN yes;
        ELSE
            RETURN 'f';
        END IF;
    END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION private.quiz_can_be_created(i_fk INT, i_order_number INT)
    RETURNS BOOLEAN
    AS $$
    DECLARE 
        yes BOOLEAN;
        fk_exists BOOLEAN;
    BEGIN
        SELECT COUNT(*)::int::bool FROM private.lecture WHERE id = i_fk INTO fk_exists;
        IF fk_exists THEN
            SELECT COUNT(*)::int::bool FROM private.quiz_questions WHERE fk = i_fk AND order_number = i_order_number INTO yes;
            yes = NOT yes;
            RETURN yes;
        ELSE 
            RETURN 'f';
        END IF;
    END $$ LANGUAGE plpgsql;
    """)

def drop_insert_check_functions() -> None:
    functions = [
        'grade_can_be_created',
        'subject_can_be_created',
        'branch_can_be_created',
        'lecture_can_be_created',
        'video_can_be_created',
        'game_can_be_created',
        'book_can_be_created',
        'theory_can_be_created',
        'quiz_can_be_created',
    ]

    for function in functions:
        op.execute(f"DROP FUNCTION private.{function}")


def upgrade() -> None:
    create_insert_check_functions()

def downgrade() -> None:
    drop_insert_check_functions()