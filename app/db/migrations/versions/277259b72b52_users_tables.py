"""users tables
Revision ID: 277259b72b52
Revises: e012f9ef74b1
Create Date: 2021-04-02 10:23:02.878383
"""
from alembic import op
import sqlalchemy as sa

from typing import Tuple

# revision identifiers, used by Alembic
revision = '277259b72b52'
down_revision = 'e012f9ef74b1'
branch_labels = None
depends_on = None

def timestamps(indexed: bool = False) -> Tuple[sa.Column, sa.Column]:
    return (
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
            index=indexed,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
            index=indexed,
        ),
    )


def create_user_tables() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("full_name", sa.Text, nullable=False),
        sa.Column("email", sa.Text, unique=True, nullable=False, index=True),
        sa.Column("phone_number", sa.String(20), unique=True, nullable=False),
        sa.Column("city", sa.Text, nullable=False),
        sa.Column("school", sa.Text, nullable=False),
        sa.Column("email_verified", sa.Boolean, nullable=False, server_default="False"),
        sa.Column("salt", sa.Text, nullable=False),
        sa.Column("password", sa.Text, nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="True"),
        sa.Column("is_superuser", sa.Boolean(), nullable=False, server_default="False"),
        sa.Column("jwt_token", sa.Text, nullable=True),
        sa.Column("confirmation_code", sa.String(6), nullable=True),
        schema="users"
    )
    # user - grades
    op.create_table(
        "user_grades",
        sa.Column("user_fk", sa.Integer, nullable=False),
        sa.Column("grade_fk", sa.Integer, nullable=False),
        sa.Column("days_left", sa.Integer, nullable=False),
        sa.Column("for_life", sa.Boolean, nullable=False, server_default="False"),
        *timestamps(),
        sa.ForeignKeyConstraint(['user_fk'], ['users.users.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['grade_fk'], ['private.grade.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.UniqueConstraint('user_fk', 'grade_fk'),
        schema='users'
    )
    # user - subjects
    op.create_table(
        "user_subjects",
        sa.Column("user_fk", sa.Integer(), nullable=False),
        sa.Column("subject_fk", sa.Integer(), nullable=False),
        sa.Column("days_left", sa.Integer(), nullable=False),
        sa.Column("for_life", sa.Boolean, nullable=False, server_default="False"),
        *timestamps(),
        sa.ForeignKeyConstraint(['user_fk'], ['users.users.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['subject_fk'], ['private.subject.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.UniqueConstraint('user_fk', 'subject_fk'),
        schema='users'
    )

    # TRIGGERS

    # after insert on grades function
    op.execute("""
    CREATE OR REPLACE FUNCTION users.insert_subject_after_grade_trigger_function() RETURNS TRIGGER
    AS $$
    DECLARE
        _row RECORD;
    BEGIN
        FOR _row IN SELECT private.subject.id FROM private.subject WHERE private.subject.fk = NEW.grade_fk LOOP
            INSERT INTO users.user_subjects VALUES (NEW.user_fk, _row.id, NEW.days_left, NEW.for_life, NEW.created_at, NEW.updated_at)
            ON CONFLICT (user_fk, subject_fk) DO
            UPDATE
                SET
                    updated_at = NEW.updated_at,
                    days_left = NEW.days_left,
                    for_life = NEW.for_life
            WHERE users.user_subjects.subject_fk = _row.id;
        END LOOP;
    RETURN NEW;
    END $$ LANGUAGE plpgsql
    """)
    # after insert on grades trigger
    op.execute("""
    CREATE TRIGGER insert_subject_after_grade_trigger AFTER INSERT ON users.user_grades
    FOR EACH ROW EXECUTE PROCEDURE users.insert_subject_after_grade_trigger_function();
    """)

    # after delete on grades function
    op.execute("""
    CREATE OR REPLACE FUNCTION users.delete_subject_after_grade_trigger_function() RETURNS TRIGGER
    AS $$
    DECLARE
        _row RECORD;
    BEGIN
        FOR _row IN SELECT private.subject.id FROM private.subject WHERE private.subject.fk = OLD.grade_fk LOOP
            DELETE FROM users.user_subjects WHERE subject_fk = _row.id;
        END LOOP;
    RETURN NEW;
    END $$ LANGUAGE plpgsql
    """)
    # after delete on grades trigger
    op.execute("""
    CREATE TRIGGER delete_subject_after_grade_trigger AFTER DELETE ON users.user_grades
    FOR EACH ROW EXECUTE PROCEDURE users.delete_subject_after_grade_trigger_function();
    """)


def drop_users_tables() -> None:
    op.execute("DROP TABLE users.user_subjects")
    op.execute("DROP TABLE users.user_grades")
    op.execute("DROP TABLE users.users")
    op.execute("DROP FUNCTION users.delete_subject_after_grade_trigger_function")
    op.execute("DROP FUNCTION users.insert_subject_after_grade_trigger_function")


def upgrade() -> None:
    create_user_tables()

def downgrade() -> None:
    drop_users_tables()