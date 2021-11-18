"""deleting_account_strategy
Revision ID: 5530af02dfea
Revises: 0060361b63fe
Create Date: 2021-11-16 10:16:48.759358
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '5530af02dfea'
down_revision = '0060361b63fe'
branch_labels = None
depends_on = None


def profile_reactivation() -> None:
    op.create_table(
        "reactivation_hashes",
        sa.Column("user_fk", sa.Integer, primary_key=True),
        sa.Column("reactivation_hash", sa.String(64), nullable=False),
        sa.ForeignKeyConstraint(["user_fk"], ["users.users.id"], ondelete='CASCADE'),
        sa.UniqueConstraint("user_fk"),
        schema="users"
    )

    op.execute("""
    CREATE OR REPLACE FUNCTION users.create_reactivation_request(id_ INT)
    RETURNS VARCHAR(64)
    AS $$
    DECLARE
        secret TEXT;
    BEGIN
        IF (SELECT COUNT(*) FROM users.users WHERE id = id_ AND is_active = 'f') = 0 THEN
            RETURN NULL;
        END IF;

        IF (SELECT COUNT(reactivation_hash) FROM users.reactivation_hashes WHERE user_fk = id_) > 0 THEN
            RETURN (SELECT reactivation_hash FROM users.reactivation_hashes WHERE user_fk = id_);
        ELSE
            SELECT TO_CHAR(now(), 'YYYYMMDDhhmmss') INTO secret;
            secret = CONCAT(secret, (SELECT email FROM users.users WHERE id = id_));
            INSERT INTO users.reactivation_hashes(user_fk, reactivation_hash) VALUES (id_, ENCODE(sha256(secret::bytea), 'hex'));
            RETURN (SELECT reactivation_hash FROM users.reactivation_hashes WHERE user_fk = id_);
        END IF;
    END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION users.activate_profile(reactivation_hash_ VARCHAR(64))
    RETURNS BOOLEAN
    AS $$
    DECLARE 
        user_id INT;
    BEGIN
        IF (SELECT COUNT(*) FROM users.reactivation_hashes WHERE reactivation_hash = reactivation_hash_) > 0 THEN
            SELECT user_fk INTO user_id FROM users.reactivation_hashes WHERE reactivation_hash = reactivation_hash_;
            UPDATE users.users SET is_active = 't', deactivated = NULL WHERE id = user_id;
            DELETE FROM users.reactivation_hashes WHERE user_fk = user_id;
            RETURN 't';
        ELSE
            RETURN 'f';
        END IF;
    END $$ LANGUAGE plpgsql;
    """)

def remove_triggers_for_order_numbers() -> None:
    triggers = [
        'update_about_us_order_numbers_after_delete_trigger ON public.about_us',
        'update_instruction_order_numbers_after_delete_trigger ON public.instruction',
    ]

    for trigger in triggers:
        op.execute(f"DROP TRIGGER IF EXISTS {trigger}")

    procedures = [
        'update_about_us_order_numbers_after_delete',
        'update_instruction_order_numbers_after_delete',
    ]

    for proc in procedures:
        op.execute(f"DROP FUNCTION IF EXISTS public.{proc} CASCADE")


def profile_deactivation() -> None:
    op.execute("""
    ALTER TABLE users.users ADD COLUMN deactivated TIMESTAMP;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION users.deactivate_profile(id_ INT)
    RETURNS VOID
    AS $$
    BEGIN
        UPDATE users.users SET is_active = 'f', deactivated = now() WHERE id = id_;
    END $$ LANGUAGE plpgsql;
    """)


def profile_deletion() -> None:
    op.execute("""
    CREATE OR REPLACE FUNCTION users.delete_profile(id_ INT)
    RETURNS VOID
    AS $$ 
    BEGIN
        DELETE FROM users.users WHERE id = id_;
    END $$ LANGUAGE plpgsql;
    """)

def views() -> None:
    op.execute("""
    CREATE VIEW users.profiles_for_warning_month_view AS
    SELECT id, email FROM users.users WHERE is_active = 'f' AND deactivated::date = (now() - INTERVAL '2 months')::date;
    """)

    op.execute("""
    CREATE VIEW users.profiles_for_warning_week_view AS
    SELECT id, email FROM users.users WHERE is_active = 'f' AND (now() - INTERVAL'3 months' + INTERVAL'7 days')::date = deactivated::date;
    """)

    op.execute("""
    CREATE VIEW users.profiles_for_deletion_view AS
    SELECT id, email FROM users.users WHERE is_active = 'f' AND deactivated < now() - INTERVAL '3 months';
    """)

def drop_views() -> None:
    views = [
        'profiles_for_warning_month_view',
        'profiles_for_warning_week_view',
        'profiles_for_deletion_view',
    ]

    for view in views:
        op.execute(f"DROP VIEW users.{view}")


def drop_functions() -> None:
    functions = [
        'deactivate_profile',
        'activate_profile',
        'delete_profile',
        'create_reactivation_request',
    ]

    for function in functions:
        op.execute(f"DROP FUNCTION users.{function}")

    op.execute("""
    ALTER TABLE users.users DROP COLUMN deactivated;
    """)
    op.execute("DROP TABLE users.reactivation_hashes")

def upgrade() -> None:
    remove_triggers_for_order_numbers()
    profile_deactivation()
    profile_deletion()
    profile_reactivation()
    views()

def downgrade() -> None:
    drop_views()
    drop_functions()
