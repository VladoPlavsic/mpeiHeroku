"""users functions
Revision ID: dc0130a0b54b
Revises: 277259b72b52
Create Date: 2021-04-02 11:25:10.407333
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = 'dc0130a0b54b'
down_revision = '277259b72b52'
branch_labels = None
depends_on = None

def create_user_functions() -> None:
    # create new user
    op.execute("""
    CREATE OR REPLACE FUNCTION users.create_user_function(
        i_full_name text, 
        i_email text, 
        i_phone_number varchar(20),
        i_city text,
        i_school text,
        i_salt text, 
        i_password text, 
        i_email_verified boolean default 'f',
        i_is_active boolean default 'f',
        i_is_superuser boolean default 'f',
        i_jwt_token text default null,
        i_confirmation_code varchar(6) default null)
    RETURNS TABLE (id int, full_name text, email text, phone_number varchar(20), city text, school text, password text, salt text, confirmation_code varchar(6), jwt_token text)
    AS $$
    DECLARE 
        inserted_id int;
    BEGIN
        INSERT INTO users.users (
            full_name,
            email,
            phone_number,
            city,
            school,
            email_verified,
            salt,
            password,
            is_active,
            is_superuser,
            jwt_token,
            confirmation_code)
        VALUES (
            i_full_name,
            i_email,
            i_phone_number,
            i_city,
            i_school,
            i_email_verified,
            i_salt,
            i_password,
            i_is_active,
            i_is_superuser,
            i_jwt_token,
            i_confirmation_code) RETURNING users.users.id INTO inserted_id;
        RETURN QUERY (SELECT
            users.users.id, 
            users.users.full_name, 
            users.users.email,
            users.users.phone_number,
            users.users.city,
            users.users.school,
            users.users.password,
            users.users.salt,
            users.users.confirmation_code,
            users.users.jwt_token
            FROM users.users WHERE users.users.id = inserted_id);
    END $$ LANGUAGE plpgsql;
    """)

   
    # get user by email
    op.execute("""
    CREATE OR REPLACE FUNCTION users.get_user_by_email(i_email text)
    RETURNS TABLE (id int, full_name text, email text, phone_number varchar(20), city text, school text, password text, salt text, jwt text, confirmation_code varchar(6), is_active boolean, email_verified boolean, is_superuser boolean)
    AS $$
    BEGIN 
            RETURN QUERY (SELECT
            users.users.id, 
            users.users.full_name, 
            users.users.email,
            users.users.phone_number,
            users.users.city, 
            users.users.school, 
            users.users.password,
            users.users.salt,
            users.users.jwt_token,
            users.users.confirmation_code,
            users.users.is_active,
            users.users.email_verified,
            users.users.is_superuser
            FROM users.users WHERE users.users.email = i_email);
    END $$ LANGUAGE plpgsql;
    """)

def create_user_authentication_functions() -> None:
    # set confirmation code
    op.execute(
    """
    CREATE OR REPLACE FUNCTION users.set_confirmation_code(user_id int, i_confirmation varchar(6))
    RETURNS VOID
    AS $$
    BEGIN
        UPDATE users.users SET
            confirmation_code = i_confirmation
        WHERE users.users.id = user_id;
    END $$ LANGUAGE plpgsql;
    """)

    # set jwt token
    op.execute(
    """
    CREATE OR REPLACE FUNCTION users.set_jwt_token(user_id int, token text)
    RETURNS VOID
    AS $$
    BEGIN 
        UPDATE users.users SET
            jwt_token = token,
            is_active = 't'
        WHERE users.users.id = user_id;
    END $$ LANGUAGE plpgsql;
    """)

    # verify email
    op.execute(
    """
    CREATE OR REPLACE FUNCTION users.verify_email(user_id int)
    RETURNS VOID
    AS $$
    BEGIN 
        UPDATE users.users SET
            email_verified = 't'
        WHERE users.users.id = user_id;
    END $$ LANGUAGE plpgsql;
    """
    )


def delete_users_functions() -> None:
    functions = [
        'create_user_function',
        'get_user_by_email',
        'set_confirmation_code',
        'set_jwt_token',
        'verify_email',
        ]

    for function in functions:
        op.execute(f"DROP FUNCTION users.{function}")

def upgrade() -> None:
    create_user_functions()
    create_user_authentication_functions()

def downgrade() -> None:
    delete_users_functions()