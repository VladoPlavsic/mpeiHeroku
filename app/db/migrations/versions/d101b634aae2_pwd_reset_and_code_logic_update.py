"""pwd_reset_and_code_logic_update
Revision ID: d101b634aae2
Revises: c6bc3c236bec
Create Date: 2021-06-09 09:57:27.215402
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = 'd101b634aae2'
down_revision = 'c6bc3c236bec'
branch_labels = None
depends_on = None

def update_login_logic() -> None:
    # remove confirmation code from users table
    op.execute("""
    ALTER TABLE users.users
    DROP COLUMN confirmation_code;
    """)
    # and create new table for storing them
    op.create_table(
        "codes",
        sa.Column("user_fk", sa.Integer, primary_key=True),
        sa.Column("confirmation_code", sa.String(6), nullable=False),
        sa.Column("expiration", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_fk"], ["users.users.id"], ondelete='CASCADE'),
        schema="users"
    )
    
    # update set confirmation code function
    op.execute(
        "DROP FUNCTION users.set_confirmation_code;"
    )

    #NOTE: don't drop this function on downgrade!
    op.execute(
    """
    CREATE OR REPLACE FUNCTION users.set_confirmation_code(user_id int, i_confirmation varchar(6))
    RETURNS VARCHAR(6)
    AS $$
    DECLARE 
        expiration_date TIMESTAMP;
        exists INT;
        code VARCHAR(6);
    BEGIN
        SELECT expiration INTO expiration_date FROM users.codes WHERE user_fk = user_id;
        SELECT COUNT(*) INTO exists FROM users.codes WHERE user_fk = user_id;
        IF exists = 0 or expiration_date < now() THEN
            DELETE FROM users.codes WHERE user_fk = user_id;
            INSERT INTO users.codes VALUES(user_id, i_confirmation, now() + interval '3 minute');
        END IF;
        SELECT confirmation_code INTO code FROM users.codes WHERE user_fk = user_id;
        RETURN code;
    END $$ LANGUAGE plpgsql;
    """)

    # update create user function
    op.execute("DROP FUNCTION users.create_user_function")

    # NOTE: don't drop this function on downgrade
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
        i_jwt_token text default null)
    RETURNS TABLE (id int, full_name text, email text, phone_number varchar(20), city text, school text, password text, salt text, jwt_token text)
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
            jwt_token)
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
            i_jwt_token) RETURNING users.users.id INTO inserted_id;
        RETURN QUERY (SELECT
            users.users.id, 
            users.users.full_name, 
            users.users.email,
            users.users.phone_number,
            users.users.city,
            users.users.school,
            users.users.password,
            users.users.salt,
            users.users.jwt_token
            FROM users.users WHERE users.users.id = inserted_id);
    END $$ LANGUAGE plpgsql;
    """)

    # update get user by email
    op.execute("DROP FUNCTION users.get_user_by_email")

    op.execute("""
    CREATE OR REPLACE FUNCTION users.get_user_by_email(i_email text)
    RETURNS TABLE (id int, full_name text, email text, phone_number varchar(20), city text, school text, password text, salt text, jwt text, is_active boolean, email_verified boolean, is_superuser boolean)
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
            users.users.is_active,
            users.users.email_verified,
            users.users.is_superuser
            FROM users.users WHERE users.users.email = i_email);
    END $$ LANGUAGE plpgsql;
    """)


    # check confirmation code function
    op.execute("""
    CREATE OR REPLACE FUNCTION users.check_confirmation_code(user_id INT, i_confirmation_code VARCHAR(6))
    RETURNS BOOLEAN
    AS $$
    DECLARE 
        expiration_date TIMESTAMP;
        code VARCHAR(6);
    BEGIN   
        SELECT confirmation_code, expiration INTO code, expiration_date FROM users.codes WHERE user_fk = user_id;
        IF expiration_date < now() or code != i_confirmation_code THEN
            RETURN 'f';
        END IF;
        DELETE FROM users.codes WHERE user_fk = user_id;
        RETURN 't';
    END $$ LANGUAGE plpgsql;
    """)


def downgrade_login_logic() -> None:
    op.execute("""
    ALTER TABLE users.users
    ADD COLUMN confirmation_code VARCHAR(6);
    """)
    op.execute("DROP TABLE users.codes")
    op.execute("DROP FUNCTION users.check_confirmation_code")

def recovery_tables() -> None:
    # recovery keys table
    op.create_table(
        "recovery_keys",
        sa.Column("user_fk", sa.Integer, primary_key=True),
        sa.Column("recovery_key", sa.String(64), nullable=False),
        sa.ForeignKeyConstraint(["user_fk"], ["users.users.id"], ondelete="CASCADE", onupdate="CASCADE"),
        sa.UniqueConstraint("user_fk"),
        schema="users"
    )
    # recovery hashes table
    op.create_table(
        "recovery_hashes",
        sa.Column("user_fk", sa.Integer, primary_key=True),
        sa.Column("recovery_hash", sa.String(64), nullable=False),
        sa.ForeignKeyConstraint(["user_fk"], ["users.users.id"], ondelete="CASCADE", onupdate="CASCADE"),
        sa.UniqueConstraint("user_fk"),
        schema="users"
    )

def drop_recovery_tables() -> None:
    op.execute("DROP TABLE users.recovery_keys") 
    op.execute("DROP TABLE users.recovery_hashes") 

def recovery_functions() -> None:
    # create recovery request
    # create new recovery key for user
    op.execute("""
    CREATE OR REPLACE FUNCTION users.create_recovery_request(i_email text)
    RETURNS VARCHAR(64)
    AS $$
    DECLARE
        secret TEXT;
        key VARCHAR(64);
        user_ INT;
    BEGIN
        IF (SELECT COUNT(*) FROM users.users WHERE email = i_email) = 0 THEN
            RETURN null;
        END IF;
        SELECT id INTO user_ FROM users.users WHERE email = i_email;
        SELECT TO_CHAR(now(), 'YYYYMMDDhhmmss') INTO secret;
        secret = CONCAT(secret, i_email);
        SELECT ENCODE(sha256(secret::bytea), 'hex') INTO key;
        INSERT INTO users.recovery_keys VALUES(user_, key) ON CONFLICT (user_fk) DO UPDATE SET recovery_key = key;
        RETURN key;
    END $$ LANGUAGE plpgsql;
    """)
    # check recovery request key
    op.execute("""
    CREATE OR REPLACE FUNCTION users.check_recovery_request(i_email text, i_key VARCHAR(64))
    RETURNS VARCHAR(64)
    AS $$
    DECLARE
        user_ INT;
        key VARCHAR(64);
        hash VARCHAR(64);
    BEGIN
        IF (SELECT COUNT(*) FROM users.users WHERE email = i_email) = 0 THEN
            RETURN null;
        END IF;
        SELECT id INTO user_ FROM users.users WHERE email = i_email;
        SELECT recovery_key INTO key FROM users.recovery_keys WHERE user_fk = user_;
        IF key != i_key THEN
            RETURN null;
        ELSE
            DELETE FROM users.recovery_keys WHERE user_fk = user_;
            SELECT ENCODE(sha256(key::bytea), 'hex') INTO hash;
            INSERT INTO users.recovery_hashes VALUES(user_, hash) ON CONFLICT (user_fk) DO UPDATE SET recovery_hash = hash RETURNING recovery_hash INTO key;
            RETURN key;
        END IF;
    END $$ LANGUAGE plpgsql;
    """)
    # update password
    op.execute("""
    CREATE OR REPLACE FUNCTION users.update_password(i_hash VARCHAR(64), i_password TEXT, i_salt TEXT)
    RETURNS BOOLEAN
    AS $$
    DECLARE
        user_ INT;
    BEGIN
        SELECT user_fk INTO user_ FROM users.recovery_hashes WHERE recovery_hash = i_hash;
        IF (SELECT COUNT(*) FROM users.users WHERE id = user_) = 0 THEN
            RETURN 'f';
        ELSE
            UPDATE users.users SET 
                password = i_password,
                salt = i_salt
            WHERE id = user_;
            DELETE FROM users.recovery_hashes WHERE user_fk = user_;
            RETURN 't';
        END IF;
    END $$ LANGUAGE plpgsql;
    """)


def drop_recovery_functions() -> None:
    functions = [
        "create_recovery_request",
        "check_recovery_request",
        "update_password"
    ]

    for function in functions:
        op.execute(f"DROP FUNCTION users.{function} CASCADE")

def upgrade() -> None:
    update_login_logic()
    recovery_tables()
    recovery_functions()

def downgrade() -> None:
    downgrade_login_logic()
    drop_recovery_tables()
    drop_recovery_functions()
