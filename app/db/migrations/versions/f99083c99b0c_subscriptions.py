"""Subscriptions
Revision ID: f99083c99b0c
Revises: b88c1a85ee72
Create Date: 2021-05-25 13:39:59.868052
"""
from sqlalchemy import schema
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = 'f99083c99b0c'
down_revision = 'b88c1a85ee72'
branch_labels = None
depends_on = None

def create_tables() -> None:
    op.create_table(
        "grade_subscription_plans",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(50), nullable=False),
        sa.Column("price", sa.types.Numeric(precision=20, scale=2), nullable=False),
        sa.Column("month_count", sa.Integer, nullable=False),
        schema="subscriptions"
    )

    op.create_table(
        "subject_subscription_plans",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(50), nullable=False),
        sa.Column("price", sa.types.Numeric(precision=20, scale=2), nullable=False),
        sa.Column("month_count", sa.Integer, nullable=False),
        schema="subscriptions"
    )

    op.create_table(
        "grade_offers",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("grade_fk", sa.Integer, nullable=False),
        sa.Column("subscription_fk", sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(["grade_fk"], ["private.grade.id"], onupdate='CASCADE', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['subscription_fk'], ['subscriptions.grade_subscription_plans.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.UniqueConstraint('grade_fk', 'subscription_fk'),
        schema="subscriptions"
    )

    op.create_table(
        "subject_offers",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("subject_fk", sa.Integer, nullable=False),
        sa.Column("subscription_fk", sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(["subject_fk"], ["private.subject.id"], onupdate='CASCADE', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['subscription_fk'], ['subscriptions.subject_subscription_plans.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.UniqueConstraint('subject_fk', 'subscription_fk'),
        schema="subscriptions"
    )

    op.create_table(
        "pending_subscriptions",
        sa.Column("user_fk", sa.Integer, nullable=False),
        sa.Column("offer_fk", sa.Integer, nullable=False),
        sa.Column("payment_id", sa.Text, primary_key=True),
        sa.Column("level", sa.Boolean, nullable=False),
        sa.UniqueConstraint('user_fk', 'offer_fk', 'level'),
        schema="subscriptions"
    )

def drop_tables() -> None:
    op.execute("DROP TABLE subscriptions.pending_subscriptions")
    op.execute("DROP TABLE subscriptions.subject_offers")
    op.execute("DROP TABLE subscriptions.grade_offers")
    op.execute("DROP TABLE subscriptions.grade_subscription_plans")
    op.execute("DROP TABLE subscriptions.subject_subscription_plans")


# triggers
def create_triggers() -> None:
    # ###
    # GRADES
    # ###
    #triegger function
    op.execute("""
    CREATE OR REPLACE FUNCTION subscriptions.insert_plans_after_grade_trigger_function() RETURNS TRIGGER
    AS $$
    DECLARE
        _row RECORD;
    BEGIN
        FOR _row IN SELECT id FROM subscriptions.grade_subscription_plans LOOP
            INSERT INTO subscriptions.grade_offers (grade_fk, subscription_fk) VALUES(NEW.id, _row.id);
        END LOOP;
    RETURN NEW;
    END $$ LANGUAGE plpgsql
    """)
    # trigger
    op.execute("""
    CREATE TRIGGER insert_plans_after_grade_trigger AFTER INSERT ON private.grade
    FOR EACH ROW EXECUTE PROCEDURE subscriptions.insert_plans_after_grade_trigger_function();
    """)

    # ###
    # SUBJECTS
    # ###
    op.execute("""
    CREATE OR REPLACE FUNCTION subscriptions.insert_plans_after_subject_trigger_function() RETURNS TRIGGER
    AS $$
    DECLARE
        _row RECORD;
    BEGIN
        FOR _row IN SELECT id FROM subscriptions.subject_subscription_plans LOOP
            INSERT INTO subscriptions.subject_offers (subject_fk, subscription_fk) VALUES(NEW.id, _row.id);
        END LOOP;
    RETURN NEW;
    END $$ LANGUAGE plpgsql
    """)
    # trigger
    op.execute("""
    CREATE TRIGGER insert_plans_after_subject_trigger AFTER INSERT ON private.subject
    FOR EACH ROW EXECUTE PROCEDURE subscriptions.insert_plans_after_subject_trigger_function();
    """)


    # ###
    # PLANS
    # ###
    # GRADES
    op.execute("""
    CREATE OR REPLACE FUNCTION subscriptions.insert_offers_after_grade_plans_trigger_function() RETURNS TRIGGER
    AS $$
    DECLARE
        _row RECORD;
    BEGIN
        FOR _row IN SELECT id FROM private.grade LOOP
            INSERT INTO subscriptions.grade_offers (grade_fk, subscription_fk) VALUES (_row.id, NEW.id);
        END LOOP;
    RETURN NEW;
    END $$ LANGUAGE plpgsql;
    """)
    # trigger
    op.execute("""
    CREATE TRIGGER insert_grade_offers_after_plans_trigger AFTER INSERT ON subscriptions.grade_subscription_plans
    FOR EACH ROW EXECUTE PROCEDURE subscriptions.insert_offers_after_grade_plans_trigger_function();
    """)

    # SUBJECTS
    op.execute("""
    CREATE OR REPLACE FUNCTION subscriptions.insert_offers_after_subject_plans_trigger_function() RETURNS TRIGGER
    AS $$
    DECLARE
        _row RECORD;
    BEGIN
        FOR _row IN SELECT id FROM private.subject LOOP
            INSERT INTO subscriptions.subject_offers (grade_fk, subscription_fk) VALUES (_row.id, NEW.id);
        END LOOP;
    RETURN NEW;
    END $$ LANGUAGE plpgsql;
    """)
    # trigger
    op.execute("""
    CREATE TRIGGER insert_subject_offers_after_plans_trigger AFTER INSERT ON subscriptions.subject_subscription_plans
    FOR EACH ROW EXECUTE PROCEDURE subscriptions.insert_offers_after_subject_plans_trigger_function();
    """)




# functions
def create_subscription_functions() -> None:
    # check if user has already submited subscription request for 
    # given offer
    op.execute("""
    CREATE OR REPLACE FUNCTION subscriptions.check_subscription_pending(i_user_fk int, i_offer_fk int, i_level int)
    RETURNS INTEGER
    AS $$
    DECLARE count_ INT;
    BEGIN
        SELECT COUNT(*) INTO count_ FROM subscriptions.pending_subscriptions WHERE user_fk = i_user_fk AND offer_fk = i_offer_fk AND level = i_level::boolean;
        RETURN count_;
    END $$ LANGUAGE plpgsql;
    """)

    # create subscription request
    op.execute("""
    CREATE OR REPLACE FUNCTION subscriptions.create_subscription_pending(i_user_fk int, i_offer_fk int, i_payment_id text, i_level int)
    RETURNS VOID
    AS $$
    BEGIN
        INSERT INTO subscriptions.pending_subscriptions VALUES (i_user_fk, i_offer_fk, i_payment_id, i_level::boolean);
    END $$ LANGUAGE plpgsql;
    """)

    # get user/offer information from confirmed payment by payment id
    op.execute("""
    CREATE OR REPLACE FUNCTION subscriptions.get_subscription_pending(i_payment_id text)
    RETURNS TABLE(
        user_fk int,
        offer_fk int,
        payment_id text,
        level bool
    )
    AS $$
    BEGIN
        RETURN QUERY (SELECT * FROM subscriptions.pending_subscriptions WHERE subscriptions.pending_subscriptions.payment_id = i_payment_id);
    END $$ LANGUAGE plpgsql;
    """)

    # delete pedning subscription by payment id
    op.execute("""
    CREATE OR REPLACE FUNCTION subscriptions.delete_subscription_pending(i_payment_id text)
    RETURNS VOID
    AS $$
    BEGIN
        DELETE FROM subscriptions.pending_subscriptions WHERE payment_id = i_payment_id;
    END $$ LANGUAGE plpgsql;
    """)

    # offer detalis by level and offer_fk 
    # LEVEL: 0 - grades | 1 - subjects
    op.execute("""
    CREATE OR REPLACE FUNCTION subscriptions.get_offer_details(i_level int, i_offer_fk int)
    RETURNS TABLE (
        id INT, 
        product_fk INT,
        subscription_fk INT
    )
    AS $$
    BEGIN
        IF i_level = 1 THEN
            RETURN QUERY (SELECT * FROM subscriptions.subject_offers WHERE subscriptions.subject_offers.id = i_offer_fk);
        ELSEIF i_level = 0 THEN
            RETURN QUERY (SELECT * FROM subscriptions.grade_offers WHERE subscriptions.grade_offers.id = i_offer_fk);
        ELSE
            RAISE EXCEPTION 'Unknown offer level! Level: (%)', i_level;
        END IF;
    END $$ LANGUAGE plpgsql;
    """)

    # plan details by level and id
    # LEVEL: 0 - grades | 1 - subjects
    op.execute("""
    CREATE OR REPLACE FUNCTION subscriptions.get_plan_details(i_level int, i_plan_fk int)
    RETURNS TABLE (
        id INT,
        name VARCHAR(50),
        price NUMERIC(20, 2),
        month_count INT
    )
    AS $$
    BEGIN
        IF i_level = 1 THEN
            RETURN QUERY (SELECT * FROM subscriptions.subject_subscription_plans WHERE subscriptions.subject_subscription_plans.id = i_plan_fk);
        ELSEIF i_level = 0 THEN
            RETURN QUERY (SELECT * FROM subscriptions.grade_subscription_plans WHERE subscriptions.grade_subscription_plans.id = i_plan_fk);
        ELSE
            RAISE EXCEPTION 'Unknown offer level! Level: (%)', i_level;
        END IF;
    END $$ LANGUAGE plpgsql;
    """)

    # GET AVAILABLE OFFERS
    # grades
    op.execute("""
    CREATE OR REPLACE FUNCTION subscriptions.get_available_grade_offers()
    RETURNS TABLE(
        id INT,
        name_en VARCHAR(20),
        name VARCHAR(50),
        price NUMERIC(20, 2),
        month_count INT
    )
    AS $$
    BEGIN
        RETURN QUERY (SELECT go.id, gd.name_en, su.name, su.price, su.month_count FROM subscriptions.grade_offers AS go 
        INNER JOIN private.grade AS gd ON go.grade_fk = gd.id INNER JOIN subscriptions.grade_subscription_plans AS su ON go.subscription_fk = su.id);
    END $$ LANGUAGE plpgsql;
    """)
    # subjects
    op.execute("""
    CREATE OR REPLACE FUNCTION subscriptions.get_available_subject_offers()
    RETURNS TABLE(
        id INT,
        name_en VARCHAR(20),
        name VARCHAR(50),
        price NUMERIC(20, 2),
        month_count INT
    )
    AS $$
    BEGIN
        RETURN QUERY (SELECT so.id, sd.name_en, su.name, su.price, su.month_count FROM subscriptions.subject_offers AS so 
        INNER JOIN private.subject AS sd ON so.subject_fk = sd.id INNER JOIN subscriptions.subject_subscription_plans AS su ON so.subscription_fk = su.id);
    END $$ LANGUAGE plpgsql;
    """)
    

    # GET AVAILABLE SUBSCRIPTION PLANS
    # grades
    op.execute("""
    CREATE OR REPLACE FUNCTION subscriptions.get_available_grade_plans()
    RETURNS TABLE(
        id INT,
        name VARCHAR(50),
        price NUMERIC(20, 2),
        month_count INT
    )
    AS $$
    BEGIN
        RETURN QUERY (SELECT * FROM subscriptions.grade_subscription_plans);
    END $$ LANGUAGE plpgsql;
    """)
    # subjects
    op.execute("""
    CREATE OR REPLACE FUNCTION subscriptions.get_available_subject_plans()
    RETURNS TABLE(
        id INT,
        name VARCHAR(50),
        price NUMERIC(20, 2),
        month_count INT
    )
    AS $$
    BEGIN
        RETURN QUERY (SELECT * FROM subscriptions.subject_subscription_plans);
    END $$ LANGUAGE plpgsql;
    """)

    # INSERT AVAILABLE SUBSCRIPTION PLANS
    # grades
    op.execute("""
    CREATE OR REPLACE FUNCTION subscriptions.insert_available_grade_plans(i_name VARCHAR(50), i_price NUMERIC(20, 2), i_month_count INT)
    RETURNS VOID
    AS $$
    BEGIN
        INSERT INTO subscriptions.grade_subscription_plans (name, price, month_count) VALUES (i_name, i_price, i_month_count);
    END $$ LANGUAGE plpgsql;
    """)
    # subjects
    op.execute("""
    CREATE OR REPLACE FUNCTION subscriptions.insert_available_subject_plans(i_name VARCHAR(50), i_price NUMERIC(20, 2), i_month_count INT)
    RETURNS VOID
    AS $$
    BEGIN
        INSERT INTO subscriptions.subject_subscription_plans (name, price, month_count) VALUES (i_name, i_price, i_month_count);
    END $$ LANGUAGE plpgsql;
    """)

    # DELETE AVAILABLE SUBSCRIPTION PLANS
    # grades
    op.execute("""
    CREATE OR REPLACE FUNCTION subscriptions.delete_available_grade_plans(i_id INT)
    RETURNS VOID
    AS $$
    BEGIN
        DELETE FROM subscriptions.grade_subscription_plans WHERE id = i_id;
    END $$ LANGUAGE plpgsql;
    """)
    # subjects
    op.execute("""
    CREATE OR REPLACE FUNCTION subscriptions.delete_available_subject_plans(i_id INT)
    RETURNS VOID
    AS $$
    BEGIN
        DELETE FROM subscriptions.subject_subscription_plans WHERE id = i_id;
    END $$ LANGUAGE plpgsql;
    """)


def drop_functions() -> None:
    functions = [
        'get_subscription_pending',
        'check_subscription_pending',
        'delete_subscription_pending',
        'insert_plans_after_grade_trigger_function',
        'insert_plans_after_subject_trigger_function',
        'insert_offers_after_grade_plans_trigger_function',
        'insert_offers_after_subject_plans_trigger_function',
        'get_offer_details',
        'create_subscription_pending',
        'get_available_grade_offers',
        'get_available_subject_offers',
        'get_available_subject_plans',
        'get_available_grade_plans',
        'insert_available_grade_plans',
        'insert_available_subject_plans',
        'delete_available_grade_plans',
        'delete_available_subject_plans',
        'get_plan_details',
    ]

    for function in functions:
        op.execute(f"DROP FUNCTION subscriptions.{function} CASCADE")


def upgrade() -> None:
    create_tables()
    create_triggers()
    create_subscription_functions()

def downgrade() -> None:
    drop_tables()
    drop_functions()