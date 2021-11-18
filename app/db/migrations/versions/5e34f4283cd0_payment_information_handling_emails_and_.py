"""payment_information_handling_emails_and_history
Revision ID: 5e34f4283cd0
Revises: c27dd31a70ad
Create Date: 2021-11-07 12:31:24.002293
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '5e34f4283cd0'
down_revision = 'c27dd31a70ad'
branch_labels = None
depends_on = None

def create_tables() -> None:
    # grade subscriptions history table
    op.create_table(
        "grade_subscriptions",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("grade_fk", sa.Integer, nullable=False),
        sa.Column("user_fk", sa.Integer, nullable=False),
        sa.Column("price", sa.Integer, nullable=False),
        sa.Column("purchased_at",  sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("month_count",  sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(['user_fk'], ['users.users.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['grade_fk'], ['private.grade.id'], onupdate='CASCADE', ondelete='NO ACTION'),
        schema='history'
    )

    # subject subscriptions history table
    op.create_table(
        "subject_subscriptions",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("subject_fk", sa.Integer, nullable=False),
        sa.Column("user_fk", sa.Integer, nullable=False),
        sa.Column("price", sa.Integer, nullable=False),
        sa.Column("purchased_at",  sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("month_count",  sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(['user_fk'], ['users.users.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['subject_fk'], ['private.subject.id'], onupdate='CASCADE', ondelete='NO ACTION'),
        schema='history'
    )

def upgrade() -> None:
    create_tables()

    op.execute("""
    CREATE OR REPLACE FUNCTION users.get_user_by_id(i_id INT)
    RETURNS TABLE (id int, full_name text, email text, phone_number varchar(20), city text, school text, password text, salt text, jwt text, is_active boolean, email_verified boolean, is_superuser boolean)
    AS $$
    BEGIN 
            RETURN QUERY (SELECT
            users.users.id, 
            users.users.full_name, 
            users.users.email,
            users.users.phone_number,
            users.users.city, 
            users.users.school, 
            users.users.password,
            users.users.salt,
            users.users.jwt_token,
            users.users.is_active,
            users.users.email_verified,
            users.users.is_superuser
            FROM users.users WHERE users.users.id = i_id);
    END $$ LANGUAGE plpgsql;
    """)

    op.execute("DROP FUNCTION users.add_grade_to_user")
    op.execute("DROP FUNCTION users.add_subject_to_user")

    op.execute("""
    CREATE OR REPLACE FUNCTION users.add_grade_to_user(i_user_id int, i_grade_id int, i_subscription_fk int)
    RETURNS TABLE(for_life BOOLEAN, expiration_date TIMESTAMP, plan_name VARCHAR(50))
    AS $$
    DECLARE
        temprow RECORD;
        i_subject_sub_fk INT;
    BEGIN
        IF (SELECT month_count FROM subscriptions.grade_subscription_plans WHERE id = i_subscription_fk) > 0 THEN
            IF (SELECT users.user_grades.expiration_date FROM users.user_grades WHERE user_fk = i_user_id) > now() THEN
                UPDATE users.user_grades SET expiration_date = (SELECT users.user_grades.expiration_date FROM users.user_grades WHERE user_fk = i_user_id) + interval '1 month' * (SELECT month_count FROM subscriptions.grade_subscription_plans WHERE id = i_subscription_fk) WHERE user_fk = i_user_id AND grade_fk = i_grade_id;
            ELSE
                INSERT INTO users.user_grades(user_fk, grade_fk, expiration_date, for_life) VALUES (i_user_id, i_grade_id, now() + interval '1 month' * (SELECT month_count FROM subscriptions.grade_subscription_plans WHERE id = i_subscription_fk), 'f');
            END IF;
        ELSE
            INSERT INTO users.user_grades(user_fk, grade_fk, expiration_date, for_life) VALUES (i_user_id, i_grade_id, now(), 't') ON CONFLICT ON CONSTRAINT user_grades_user_fk_grade_fk_key DO UPDATE SET for_life = 't';
        END IF;
        INSERT INTO history.grade_subscriptions(grade_fk, user_fk, price, purchased_at, month_count) VALUES(i_grade_id, i_user_id, (SELECT price FROM subscriptions.grade_subscription_plans WHERE id = i_subscription_fk), now(), (SELECT month_count FROM subscriptions.grade_subscription_plans WHERE id = i_subscription_fk));
        SELECT subscriptions.subject_subscription_plans.id INTO i_subject_sub_fk FROM subscriptions.subject_subscription_plans WHERE month_count = (SELECT month_count FROM subscriptions.grade_subscription_plans WHERE id = i_subscription_fk);
        FOR temprow IN
            SELECT id FROM private.subject WHERE private.subject.fk = i_subject_sub_fk
        LOOP
            PERFORM users.add_subject_to_user(i_user_id, temprow.id, i_subject_sub_fk);
        END LOOP;
        RETURN QUERY (SELECT users.user_grades.for_life, users.user_grades.expiration_date, subscriptions.grade_subscription_plans.name FROM users.user_grades INNER JOIN subscriptions.grade_subscription_plans ON id = i_subscription_fk WHERE user_fk = i_user_id AND grade_fk = i_grade_id);
    END $$ LANGUAGE plpgsql;
    """)
    # add subject to user
    op.execute("""
    CREATE OR REPLACE FUNCTION users.add_subject_to_user(i_user_id int, i_subject_id int, i_subscription_fk int)
    RETURNS TABLE(for_life BOOLEAN, expiration_date TIMESTAMP, plan_name VARCHAR(50))
    AS $$
    BEGIN
        IF (SELECT month_count FROM subscriptions.subject_subscription_plans WHERE id = i_subscription_fk) > 0 THEN
            IF (SELECT users.user_subjects.expiration_date FROM users.user_subjects WHERE user_fk = i_user_id) > now() THEN
                UPDATE users.user_subjects SET expiration_date = (SELECT users.user_subjects.expiration_date FROM users.user_subjects WHERE user_fk = i_user_id) + interval '1 month' * (SELECT month_count FROM subscriptions.subject_subscription_plans WHERE id = i_subscription_fk) WHERE user_fk = i_user_id AND subject_fk = i_subject_id;
            ELSE
                INSERT INTO users.user_subjects(user_fk, subject_fk, expiration_date, for_life) VALUES (i_user_id, i_subject_id, now() + interval '1 month' * (SELECT month_count FROM subscriptions.subject_subscription_plans WHERE id = i_subscription_fk), 'f');
            END IF;
        ELSE
            INSERT INTO users.user_subjects(user_fk, subject_fk, expiration_date, for_life) VALUES (i_user_id, i_subject_id, now(), 't') ON CONFLICT ON CONSTRAINT user_subjects_user_fk_subject_fk_key DO UPDATE SET for_life = 't';
        END IF;
        INSERT INTO history.subject_subscriptions(subject_fk, user_fk, price, purchased_at, month_count) VALUES(i_subject_id, i_user_id, (SELECT price FROM subscriptions.subject_subscription_plans WHERE id = i_subscription_fk), now(), (SELECT month_count FROM subscriptions.subject_subscription_plans WHERE id = i_subscription_fk));
        RETURN QUERY (SELECT users.user_subjects.for_life, users.user_subjects.expiration_date, subscriptions.grade_subscription_plans.name FROM users.user_subjects INNER JOIN subscriptions.grade_subscription_plans ON id = i_subscription_fk WHERE user_fk = i_user_id AND subject_fk = i_subject_id);
    END $$ LANGUAGE plpgsql;
    """)
    pass

def return_all_functions() -> None:
    op.execute("DROP FUNCTION users.add_grade_to_user")
    op.execute("DROP FUNCTION users.add_subject_to_user")

    op.execute("""
    CREATE OR REPLACE FUNCTION users.add_grade_to_user(i_user_id int, i_grade_id int, i_subscription_fk int)
    RETURNS VOID
    AS $$
    DECLARE
        temprow RECORD;
        i_subject_sub_fk INT;
    BEGIN
        IF (SELECT month_count FROM subscriptions.grade_subscription_plans WHERE id = i_subscription_fk) > 0 THEN
            IF (SELECT expiration_date FROM users.user_grades WHERE user_fk = i_user_id) > now() THEN
                UPDATE users.user_grades SET expiration_date = (SELECT expiration_date FROM users.user_grades WHERE user_fk = i_user_id) + interval '1 month' * (SELECT month_count FROM subscriptions.grade_subscription_plans WHERE id = i_subscription_fk) WHERE user_fk = i_user_id AND grade_fk = i_grade_id;
            ELSE
                INSERT INTO users.user_grades(user_fk, grade_fk, expiration_date, for_life) VALUES (i_user_id, i_grade_id, now() + interval '1 month' * (SELECT month_count FROM subscriptions.grade_subscription_plans WHERE id = i_subscription_fk), 'f');
            END IF;
        ELSE
            INSERT INTO users.user_grades(user_fk, grade_fk, expiration_date, for_life) VALUES (i_user_id, i_grade_id, now(), 't') ON CONFLICT ON CONSTRAINT user_grades_user_fk_grade_fk_key DO UPDATE SET for_life = 't';
        END IF;
        SELECT subscriptions.subject_subscription_plans.id INTO i_subject_sub_fk FROM subscriptions.subject_subscription_plans WHERE month_count = (SELECT month_count FROM subscriptions.grade_subscription_plans WHERE id = i_subscription_fk);
        FOR temprow IN
            SELECT id FROM private.subject WHERE private.subject.fk = i_grade_id
        LOOP
            PERFORM users.add_subject_to_user(i_user_id, temprow.id, i_subject_sub_fk);
        END LOOP;
    END $$ LANGUAGE plpgsql;
    """)
    # add subject to user
    op.execute("""
    CREATE OR REPLACE FUNCTION users.add_subject_to_user(i_user_id int, i_subject_id int, i_subscription_fk int)
    RETURNS VOID
    AS $$
    BEGIN
        IF (SELECT month_count FROM subscriptions.subject_subscription_plans WHERE id = i_subscription_fk) > 0 THEN
            IF (SELECT expiration_date FROM users.user_subjects WHERE user_fk = i_user_id) > now() THEN
                UPDATE users.user_subjects SET expiration_date = (SELECT expiration_date FROM users.user_subjects WHERE user_fk = i_user_id) + interval '1 month' * (SELECT month_count FROM subscriptions.subject_subscription_plans WHERE id = i_subscription_fk) WHERE user_fk = i_user_id AND subject_fk = i_subject_id;
            ELSE
                INSERT INTO users.user_subjects(user_fk, subject_fk, expiration_date, for_life) VALUES (i_user_id, i_subject_id, now() + interval '1 month' * (SELECT month_count FROM subscriptions.subject_subscription_plans WHERE id = i_subscription_fk), 'f');
            END IF;
        ELSE
            INSERT INTO users.user_subjects(user_fk, subject_fk, expiration_date, for_life) VALUES (i_user_id, i_subject_id, now(), 't') ON CONFLICT ON CONSTRAINT user_subjects_user_fk_subject_fk_key DO UPDATE SET for_life = 't';
        END IF;
    END $$ LANGUAGE plpgsql;
    """)

def drop_tables() -> None:
    op.execute("DROP TABLE history.grade_subscriptions")
    op.execute("DROP TABLE history.subject_subscriptions")

def downgrade() -> None:
    return_all_functions()
    drop_tables()
