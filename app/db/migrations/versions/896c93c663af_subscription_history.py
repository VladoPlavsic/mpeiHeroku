"""subscription_history
Revision ID: 896c93c663af
Revises: 4ba828cb90a9
Create Date: 2021-11-17 18:16:20.569372
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '896c93c663af'
down_revision = '4ba828cb90a9'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute("ALTER TABLE history.grade_subscriptions ALTER COLUMN price TYPE numeric(20, 2)")
    op.execute("ALTER TABLE history.subject_subscriptions ALTER COLUMN price TYPE numeric(20, 2)")

    op.execute("""
    CREATE OR REPLACE FUNCTION history.get_subject_subscription_history(user_id INT)
    RETURNS TABLE(name_ru VARCHAR(100), price NUMERIC(20, 2), purchased_at TIMESTAMP WITH TIME ZONE, month_count INTEGER)
    AS $$
    BEGIN
        RETURN QUERY(SELECT s.name_ru, h.price, h.purchased_at, h.month_count FROM history.subject_subscriptions AS h INNER JOIN private.subject AS s ON s.id = h.subject_fk WHERE h.user_fk = user_id);
    END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION history.get_grade_subscription_history(user_id INT)
    RETURNS TABLE(name_ru VARCHAR(100), price NUMERIC(20, 2), purchased_at TIMESTAMP WITH TIME ZONE, month_count INTEGER)
    AS $$
    BEGIN
        RETURN QUERY(SELECT g.name_ru, h.price, h.purchased_at, h.month_count FROM history.grade_subscriptions AS h INNER JOIN private.grade AS g ON g.id = h.grade_fk WHERE h.user_fk = user_id);
    END $$ LANGUAGE plpgsql;
    """)


def downgrade() -> None:
    op.execute("DROP FUNCTION history.get_grade_subscription_history")
    op.execute("DROP FUNCTION history.get_subject_subscription_history")
