"""Adding s3 video handling
Revision ID: 242510e32be9
Revises: 125b3b86120a
Create Date: 2021-06-26 10:37:02.744800
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '242510e32be9'
down_revision = '125b3b86120a'
branch_labels = None
depends_on = None

def fix_updating_video_keys_functions() -> None:
    # accidently added private.theory.key instead of private.video.key
    op.execute("DROP FUNCTION private.select_all_video_keys()")
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_all_video_keys()
        RETURNS TABLE (id int, key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT private.video.fk, private.video.key FROM private.video);
        END $$ LANGUAGE plpgsql;
    """)

    # function for updating links
    op.execute("""
    CREATE OR REPLACE FUNCTION private.update_video_links(text[], text[])
        RETURNS VOID
        AS $$
        BEGIN
        FOR INDEX IN 1 .. array_upper($1, 1)
        LOOP
            UPDATE private.video SET
            url = $2[index]
            WHERE key = $1[index];
        END LOOP;
        END $$ LANGUAGE plpgsql;
    """)

def upgrade() -> None:
    fix_updating_video_keys_functions()

def downgrade() -> None:
    pass