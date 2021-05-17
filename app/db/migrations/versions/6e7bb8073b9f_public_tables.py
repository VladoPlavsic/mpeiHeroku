"""Public tables
Revision ID: 6e7bb8073b9f
Revises: ba468a333975
Create Date: 2021-03-31 08:21:34.830812
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '6e7bb8073b9f'
down_revision = 'ba468a333975'
branch_labels = None
depends_on = None

def create_public_content_tables() -> None:
    op.create_table('game',
    sa.Column('name_ru', sa.String(length=100), nullable=False),
    sa.Column('url', sa.Text, nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.UniqueConstraint('url'),
    schema='public'
    )
    op.create_table('video',
    sa.Column('name_ru', sa.String(length=100), nullable=False),
    sa.Column('url', sa.Text, nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.UniqueConstraint('url'),
    schema='public'
    )
    # CDN Content
    op.create_table('book',
    sa.Column('name_ru', sa.String(length=100), nullable=False),
    sa.Column('url', sa.Text, nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('key', sa.Text(), nullable=False),
    sa.UniqueConstraint('url'),
    schema='public'
    )
    op.create_table('practice',
    sa.Column('name_ru', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text, nullable=True),
    sa.Column('key', sa.Text(), nullable=False),
    schema='public'
    )
    op.create_table('theory',
    sa.Column('name_ru', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text, nullable=True),
    sa.Column('key', sa.Text(), nullable=False),
    schema='public'
    )
    # ###
    # Split content
    # ###
    op.create_table('practice_audio',
    sa.Column('order', sa.Integer(), nullable=False),
    sa.Column('url', sa.Text, nullable=False),
    sa.Column('key', sa.Text(), nullable=False),
    sa.UniqueConstraint('order'),
    schema='public'
    )
    op.create_table('practice_image',
    sa.Column('order', sa.Integer(), nullable=False),
    sa.Column('url', sa.Text, nullable=False),
    sa.Column('key', sa.Text(), nullable=False),
    sa.UniqueConstraint('order'),
    schema='public'
    )
    op.create_table('theory_audio',
    sa.Column('order', sa.Integer(), nullable=False),
    sa.Column('url', sa.Text, nullable=False),
    sa.Column('key', sa.Text(), nullable=False),
    sa.UniqueConstraint('order'),
    schema='public'
    )
    op.create_table('theory_image',
    sa.Column('order', sa.Integer(), nullable=False),
    sa.Column('url', sa.Text, nullable=False),
    sa.Column('key', sa.Text(), nullable=False),
    sa.UniqueConstraint('order'),
    schema='public'
    )

def create_public_front_page_tables() -> None:
    op.create_table('about_us',
    sa.Column('order', sa.Integer(), nullable=False),
    sa.Column('title', sa.Text(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('svg', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('order'),
    sa.UniqueConstraint('order'),
    schema='public'
    )
    op.create_table('faq',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question', sa.Text(), nullable=False),
    sa.Column('answer', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('question'),
    schema='public'
    )
    op.create_table('instruction',
    sa.Column('order', sa.Integer(), nullable=False),
    sa.Column('title', sa.Text(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('order'),
    sa.UniqueConstraint('order'),
    schema='public'
    )

def drop_public_tables() -> None:
    tables = [
        'video',
        'game',
        'book',
        'practice_image',
        'practice_audio',
        'practice',
        'theory_image',
        'theory_audio',
        'theory',
        'about_us',
        'faq',
        'instruction'
    ]

    for table in tables:
        op.execute(f"DROP TABLE public.{table}")

def upgrade() -> None:
    create_public_content_tables()
    create_public_front_page_tables()

def downgrade() -> None:
    drop_public_tables()