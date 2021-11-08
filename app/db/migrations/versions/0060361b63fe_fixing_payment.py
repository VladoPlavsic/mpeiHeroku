"""Fixing payment
Revision ID: 0060361b63fe
Revises: 5e34f4283cd0
Create Date: 2021-11-07 14:27:21.636515
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '0060361b63fe'
down_revision = '5e34f4283cd0'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute("""
        ALTER TABLE subscriptions.pending_subscriptions
        ADD COLUMN confirmation_token TEXT NOT NULL
    """)

    op.execute("DROP FUNCTION subscriptions.create_subscription_pending")

    # create subscription request
    op.execute("""
    CREATE OR REPLACE FUNCTION subscriptions.create_subscription_pending(i_user_fk int, i_offer_fk int, i_payment_id text, i_level int, i_confirmation_token TEXT)
    RETURNS VOID
    AS $$
    BEGIN
        INSERT INTO subscriptions.pending_subscriptions VALUES (i_user_fk, i_offer_fk, i_payment_id, i_level::boolean, i_confirmation_token) ON CONFLICT ON CONSTRAINT pending_subscriptions_user_fk_offer_fk_level_key DO UPDATE SET payment_id = i_payment_id;
    END $$ LANGUAGE plpgsql;
    """)

    op.execute("DROP FUNCTION subscriptions.get_subscription_pending")

    # get user/offer information from confirmed payment by payment id
    op.execute("""
    CREATE OR REPLACE FUNCTION subscriptions.get_subscription_pending(i_payment_id text)
    RETURNS TABLE(
        user_fk int,
        offer_fk int,
        payment_id text,
        level bool,
        confirmation_token text
    )
    AS $$
    BEGIN
        RETURN QUERY (SELECT * FROM subscriptions.pending_subscriptions WHERE subscriptions.pending_subscriptions.payment_id = i_payment_id);
    END $$ LANGUAGE plpgsql;
    """)

def downgrade() -> None:
    op.execute("""
        ALTER TABLE subscriptions.pending_subscriptions DROP COLUMN confirmation_token
    """)