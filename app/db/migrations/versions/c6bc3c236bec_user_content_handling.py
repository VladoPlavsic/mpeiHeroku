"""User content handling
Revision ID: c6bc3c236bec
Revises: f99083c99b0c
Create Date: 2021-05-26 09:29:16.929172
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = 'c6bc3c236bec'
down_revision = 'f99083c99b0c'
branch_labels = None
depends_on = None


def drop_old_functions() -> None:
    # ###
    # Functions that used to be in users_functions migration
    # Delete them if exist on old versions.
    # ###
    functions = [
        'add_grade_to_user_function',
        'add_subject_to_user_function',
        'prolong_grade_subscription',
        'prolong_subject_subscription',
        'decrement_days_left_count',
        'delete_expired_subscriptions',
        'insert_subject_after_grade_trigger_function',
        'delete_subject_after_grade_trigger_function',
        'select_all_user_available_grades',
        'select_all_user_available_subjects',
        'remove_grade_from_user_function',
        'remove_subject_from_user_function',
    ]
    
    for function in functions:
        op.execute(f"DROP FUNCTION IF EXISTS users.{function} CASCADE")


def alter_user_tables() -> None:
    # grades
    op.execute("""
    ALTER TABLE users.user_grades 
    DROP COLUMN days_left,
    ADD COLUMN expiration_date timestamp;
    """)
    # subjects
    op.execute("""
    ALTER TABLE users.user_subjects
    DROP COLUMN days_left,
    ADD COLUMN expiration_date timestamp;
    """)

def create_handling_functions() -> None:
    # add grade to user
    op.execute("""
    CREATE OR REPLACE FUNCTION users.add_grade_to_user(i_user_id int, i_grade_id int, i_subscription_fk int)
    RETURNS VOID
    AS $$
    BEGIN
        IF (SELECT month_count FROM subscriptions.grade_subscription_plans WHERE id = i_subscription_fk) > 0 THEN
            INSERT INTO users.user_grades(user_fk, grade_fk, expiration_date, for_life) VALUES (i_user_id, i_grade_id, now() + interval '1 month' * (SELECT month_count FROM subscriptions.grade_subscription_plans WHERE id = i_subscription_fk), 'f');
        ELSE
            INSERT INTO users.user_grades(user_fk, grade_fk, expiration_date, for_life) VALUES (i_user_id, i_grade_id, now(), 't');
        END IF;
    END $$ LANGUAGE plpgsql;
    """)
    # add subject to user
    op.execute("""
    CREATE OR REPLACE FUNCTION users.add_subject_to_user(i_user_id int, i_subject_id int, i_subscription_fk int)
    RETURNS VOID
    AS $$
    BEGIN
        IF (SELECT month_count FROM subscriptions.subject_subscription_plans WHERE id = i_subscription_fk) > 0 THEN
            INSERT INTO users.user_subjects(user_fk, subject_fk, expiration_date, for_life) VALUES (i_user_id, i_subject_id, now() + interval '1 month' * (SELECT month_count FROM subscriptions.grade_subscription_plans WHERE id = i_subscription_fk), 'f');
        ELSE
            INSERT INTO users.user_subjects(user_fk, subject_fk, expiration_date, for_life) VALUES (i_user_id, i_subject_id, now(), 't');
        END IF;
    END $$ LANGUAGE plpgsql;
    """)

    # select all user available grades
    op.execute("""
    CREATE OR REPLACE FUNCTION users.select_all_user_available_grades(user_id int)
    RETURNS TABLE (grade_id int, created_at timestamp WITH TIME ZONE, updated_at timestamp WITH TIME ZONE)
    AS $$
    BEGIN
        RETURN QUERY (SELECT users.user_grades.grade_fk, users.user_grades.created_at, users.user_grades.updated_at FROM users.user_grades WHERE users.user_grades.user_fk = user_id);
    END $$ LANGUAGE plpgsql;
    """)
    # select all user available subjects
    op.execute("""
    CREATE OR REPLACE FUNCTION users.select_all_user_available_subjects(user_id int)
    RETURNS TABLE (subject_id int, created_at timestamp WITH TIME ZONE, updated_at timestamp WITH TIME ZONE)
    AS $$
    BEGIN 
        RETURN QUERY (SELECT users.user_subjects.subject_fk, users.user_subjects.created_at, users.user_subjects.updated_at FROM users.user_subjects WHERE users.user_subjects.user_fk = user_id);
    END $$ LANGUAGE plpgsql;
    """)

    # remove grade from user
    op.execute("""
    CREATE OR REPLACE FUNCTION users.remove_grade_from_user_function(user_id int, grade_id int)
    RETURNS VOID
    AS $$ 
    BEGIN 
        DELETE FROM users.user_grades WHERE users.user_grades.user_fk = user_id AND users.user_grades.grade_fk = grade_id;
    END $$ LANGUAGE plpgsql;
    """)
    # remove subject from user
    op.execute("""
    CREATE OR REPLACE FUNCTION users.remove_subject_from_user_function(user_id int, subject_id int)
    RETURNS VOID
    AS $$
    BEGIN
        DELETE FROM users.user_subjects WHERE users.user_subjects.user_fk = user_id AND users.user_subjects.subject_fk = subject_id;
    END $$ LANGUAGE plpgsql;
    """)

    # delete expired subscriptions
    op.execute("""
    CREATE OR REPLACE FUNCTION users.delete_expired_subscriptions()
    RETURNS VOID
    AS $$
    BEGIN 
        DELETE FROM users.user_grades WHERE now() > expiration_date AND for_life = 'f';
        DELETE FROM users.user_subjects WHERE now() > expiration_date AND for_life = 'f';
    END $$ LANGUAGE plpgsql;
    """)

    # prolong grade subscription duration
    op.execute("""
    CREATE OR REPLACE FUNCTION users.prolong_grade_subscription(user_id int, grade_id int, months int, for_life boolean default 'f')
    RETURNS VOID
    AS $$
    BEGIN 
        UPDATE users.user_grades SET
            expiration_date = users.user_grades.expiration_date + interval '1 month' * months,
            updated_at = now(),
            for_life = for_life
        WHERE users.user_grades.user_fk = user_id AND users.user_grades.grade_fk = grade_id;
    END $$ LANGUAGE plpgsql;
    """)
    # prolong subject subscription duration
    op.execute("""
    CREATE OR REPLACE FUNCTION users.prolong_subject_subscription(user_id int, subject_id int, months int, for_life boolean default 'f')
    RETURNS VOID
    AS $$ 
    BEGIN 
        UPDATE users.user_subjects SET
            expiration_date = users.user_subjects.days_left + interval '1 month' * months,
            updated_at = now(),
            for_life = for_life
        WHERE users.user_subjects.user_fk = user_id AND users.user_subjects.subject_fk = subject_id;
    END $$ LANGUAGE plpgsql;
    """)

def drop_functions() -> None:
    functions = [
        'add_grade_to_user',
        'add_subject_to_user',
        'prolong_grade_subscription',
        'prolong_subject_subscription',
        'delete_expired_subscriptions',
        'select_all_user_available_grades',
        'select_all_user_available_subjects',
        'remove_grade_from_user_function',
        'remove_subject_from_user_function',
    ]
    
    for function in functions:
        op.execute(f"DROP FUNCTION users.{function} CASCADE")

def alter_back_user_tables() -> None:
    # grades
    op.execute("""
    ALTER TABLE users.user_grades 
    DROP COLUMN expiration_date,
    ADD COLUMN days_left int;
    """)
    # subjects
    op.execute("""
    ALTER TABLE users.user_subjects
    DROP COLUMN expiration_date,
    ADD COLUMN days_left int;
    """)


def upgrade() -> None:
    drop_old_functions()
    alter_user_tables()
    create_handling_functions()

def downgrade() -> None:
    drop_functions()
    alter_back_user_tables()