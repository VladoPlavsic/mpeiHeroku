"""Fix for insert public theory audio stored function
Revision ID: b88c1a85ee72
Revises: 8afe04192cca
Create Date: 2021-05-20 15:58:11.611901
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = 'b88c1a85ee72'
down_revision = '8afe04192cca'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # theory audio insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION public.insert_theory_audio(int[], text[], text[])
        RETURNS TABLE ("order" int, url text, key text)
        AS $$
        BEGIN
        DELETE FROM public.theory_audio;
        INSERT INTO public.theory_audio ("order", url, key)
        SELECT unnest($1), unnest($2), unnest($3);
        RETURN QUERY (SELECT public.theory_audio."order", public.theory_audio.url, public.theory_audio.key FROM public.theory_audio);
        END $$ LANGUAGE plpgsql;
    """)

def downgrade() -> None:
    pass