"""front_page_intro_video
Revision ID: 3ddd879e1720
Revises: 877c67c2ae29
Create Date: 2021-10-10 10:52:04.241609
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '3ddd879e1720'
down_revision = '877c67c2ae29'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table('intro_video',
    sa.Column('name_ru', sa.String(length=100), nullable=True),
    sa.Column('url', sa.Text, nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('object_key', sa.Text(), nullable=True),
    sa.UniqueConstraint('url'),
    schema='public'
    )

    op.execute("""
    CREATE OR REPLACE FUNCTION public.insert_intro_video(varchar(100), text, text, text)
        RETURNS TABLE (name_ru varchar(100), url text, description text, object_key text)
        AS $$
        BEGIN
        DELETE FROM public.intro_video;
        INSERT INTO public.intro_video (name_ru, url, description, object_key) VALUES ($1, $2, $3, $4);
        RETURN QUERY (SELECT * FROM public.intro_video);
        END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION public.select_intro_video()
        RETURNS TABLE (url text, name_ru varchar(20), description text, object_key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT public.intro_video.url, public.intro_video.name_ru, public.intro_video.description, public.intro_video.object_key FROM public.intro_video);
        END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION public.update_intro_video(varchar(100), text)
        RETURNS TABLE (name_ru varchar(100), url text, description text, object_key text)
        AS $$
        BEGIN
        UPDATE public.intro_video SET
            name_ru = COALESCE($1, public.intro_video.name_ru),
            description = COALESCE($2, public.intro_video.description);
        RETURN QUERY (SELECT * FROM public.intro_video);
        END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION public.delete_intro_video()
        RETURNS TEXT
        AS $$
        DECLARE
            key text;
        BEGIN 
            DELETE FROM public.intro_video RETURNING public.intro_video.object_key INTO key;
        RETURN key;
        END $$ LANGUAGE plpgsql;
    """)

    # Auto updating
    op.execute("""
    CREATE OR REPLACE FUNCTION public.select_all_intro_video_keys()
        RETURNS TABLE (object_key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT public.intro_video.object_key FROM public.intro_video);
        END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION public.update_intro_video_links(text[], text[])
        RETURNS VOID
        AS $$
        BEGIN
        FOR INDEX IN 1 .. array_upper($1, 1)
        LOOP
            UPDATE public.intro_video SET
            url = $2[index]
            WHERE object_key = $1[index];
        END LOOP;
        END $$ LANGUAGE plpgsql;
    """)

def drop_video_procedures() -> None:
    functions = [
        "insert_intro_video",
        "select_intro_video",
        "update_intro_video",
        "delete_intro_video",
        "select_all_intro_video_keys",
        "update_intro_video_links"
    ]

def downgrade() -> None:
    op.drop_table("intro_video", schema="public")
    drop_video_procedures()
