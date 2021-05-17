"""News and about us
Revision ID: 823edd886cde
Revises: 3f7c5d1f379b
Create Date: 2021-04-06 13:48:35.510913
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '823edd886cde'
down_revision = '3f7c5d1f379b'
branch_labels = None
depends_on = None

def create_table_for_our_team() -> None:
    # order, name, role, profession, description (not all),  photo key,  photo link
    op.create_table('our_team',
    sa.Column('order', sa.Integer, nullable=False, index=True),
    sa.Column('name', sa.Text, nullable=False),
    sa.Column('role', sa.Text, nullable=False),
    sa.Column('profession', sa.Text, nullable=False),
    sa.Column('description', sa.Text, nullable=True),
    sa.Column('photo_key', sa.Text, nullable=False),
    sa.Column('photo_link', sa.Text, nullable=False),
    sa.UniqueConstraint('order'),
    schema='about'
    )

def create_contatcts_and_information_about_project() -> None:
    # html text for contacts
    op.create_table('contacts',
    sa.Column('order', sa.Integer, nullable=False, index=True),
    sa.Column('html', sa.Text, nullable=False),
    sa.UniqueConstraint('order'),
    schema='about'
    )
    # html text for about project
    op.create_table('about_project',
    sa.Column('order', sa.Integer, nullable=False, index=True),
    sa.Column('html', sa.Text, nullable=False),
    sa.UniqueConstraint('order'),
    schema='about'
    )

def drop_tables() -> None:
    op.execute("DROP TABLE about.our_team")
    op.execute("DROP TABLE about.contacts")
    op.execute("DROP TABLE about.about_project")


def upgrade() -> None:
    create_contatcts_and_information_about_project()
    create_table_for_our_team()

def downgrade() -> None:
    drop_tables()