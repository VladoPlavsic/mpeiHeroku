"""Update book and practice if no img/mp3 has to be updated
Revision ID: 3f7c5d1f379b
Revises: dc0130a0b54b
Create Date: 2021-04-06 12:32:36.463981
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '3f7c5d1f379b'
down_revision = 'dc0130a0b54b'
branch_labels = None
depends_on = None

def create_update_s3_content_without_updating_s3_functions() -> None:
    # book
    op.execute("""
    CREATE OR REPLACE FUNCTION private.update_book_metadata(i_id int, i_name_ru varchar(20), i_description text)
        RETURNS TABLE (id int, name_ru varchar(20), description text, url text, key text)
        AS $$
        BEGIN 
        UPDATE private.book SET
            name_ru = COALESCE(i_name_ru, private.book.name_ru),
            description = COALESCE(i_description, private.book.description)
        WHERE private.book.fk = i_id;
        RETURN QUERY (SELECT fk, private.book.name_ru, private.book.description, private.book.url, private.book.key FROM private.book WHERE private.book.fk = i_id);
        END $$ LANGUAGE plpgsql;
    """)

    # practice
    op.execute("""
    CREATE OR REPLACE FUNCTION private.update_practice_metadata(i_id int, i_name_ru varchar(20), i_description text)
        RETURNS TABLE (id int, name_ru varchar(20), description text)
        AS $$
        BEGIN
        UPDATE private.practice SET
            name_ru = COALESCE(i_name_ru, private.practice.name_ru),
            description = COALESCE(i_description, private.practice.description)
        WHERE private.practice.fk = i_id;
        RETURN QUERY (SELECT fk, private.practice.name_ru, private.practice.description FROM private.practice WHERE private.practice.fk = i_id);
        END $$ LANGUAGE plpgsql;
    """)

    # theory
    op.execute("""
    CREATE OR REPLACE FUNCTION private.update_theory_metadata(i_id int, i_name_ru varchar(20), i_description text)
        RETURNS TABLE (id int, name_ru varchar(20), description text)
        AS $$
        BEGIN
        UPDATE private.theory SET
            name_ru = COALESCE(i_name_ru, private.theory.name_ru),
            description = COALESCE(i_description, private.theory.description)
        WHERE private.theory.fk = i_id;
        RETURN QUERY (SELECT fk, private.theory.name_ru, private.theory.description FROM private.theory WHERE private.theory.fk = i_id);
        END $$ LANGUAGE plpgsql;
    """)



def drop_update_functions() -> None:
    functions = [
        'update_book_metadata',
        'update_practice_metadata',
        'update_theory_metadata', ]

    for function in functions:
        op.execute(f"DROP FUNCTION private.{function}")

def upgrade() -> None:
    create_update_s3_content_without_updating_s3_functions()

def downgrade() -> None:
    drop_update_functions()