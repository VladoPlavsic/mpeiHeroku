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
        sa.Column("phone_number", sa.String(20), nullable=False),
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
    # These two tables have to be altered
    # will accept expiration date in case for_life = 'f'
    # cron job will be made to check dates every day
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


def drop_users_tables() -> None:
    op.execute("DROP TABLE users.user_subjects")
    op.execute("DROP TABLE users.user_grades")
    op.execute("DROP TABLE users.users")


def upgrade() -> None:
    create_user_tables()

def downgrade() -> None:
    drop_users_tables()