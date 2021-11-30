"""front_page_and_bugs
Revision ID: db420b27b5a1
Revises: 896c93c663af
Create Date: 2021-11-24 07:04:44.933893
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = 'db420b27b5a1'
down_revision = '896c93c663af'
branch_labels = None
depends_on = None


def quiz() -> None:
    op.execute("""
    CREATE OR REPLACE FUNCTION public.check_quiz_success(i_questions INT[], i_answers INT[])
    RETURNS RECORD
    AS $$
    DECLARE
        correct BOOLEAN[];
        question_numbers INT[];
        answers TEXT[];
        correct_answers TEXT[];
        correct_answers_id INT[];
        ret RECORD;
    BEGIN
        FOR index IN 1 .. array_upper(i_questions, 1) 
        LOOP
            IF (i_answers[index]) != -1 THEN
                IF (SELECT is_true FROM public.quiz_answers WHERE public.quiz_answers.id = i_answers[index]) THEN
                    correct[index] = 't';
                    answers[index] = (SELECT answer FROM public.quiz_answers WHERE public.quiz_answers.id = i_answers[index]);
                    question_numbers[index] = (SELECT order_number FROM public.quiz_questions WHERE public.quiz_questions.id = i_questions[index]);
                    correct_answers[index] = answers[index];
                    correct_answers_id[index] = (SELECT id FROM public.quiz_answers WHERE is_true = 't' AND public.quiz_answers.fk = i_questions[index]);
                ELSE
                    correct[index] = 'f';
                    answers[index] = (SELECT answer FROM public.quiz_answers WHERE public.quiz_answers.id = i_answers[index]);
                    question_numbers[index] = (SELECT order_number FROM public.quiz_questions WHERE public.quiz_questions.id = i_questions[index]);
                    correct_answers[index] = (SELECT answer FROM public.quiz_answers WHERE is_true = 't' AND public.quiz_answers.fk = i_questions[index]);
                    correct_answers_id[index] = (SELECT id FROM public.quiz_answers WHERE is_true = 't' AND public.quiz_answers.fk = i_questions[index]);
                END IF;
            ELSE
                correct[index] = 'f';
                answers[index] = '';
                question_numbers[index] = (SELECT order_number FROM public.quiz_questions WHERE public.quiz_questions.id = i_questions[index]);
                correct_answers[index] = (SELECT answer FROM public.quiz_answers WHERE is_true = 't' AND public.quiz_answers.fk = i_questions[index]);
                correct_answers_id[index] = (SELECT id FROM public.quiz_answers WHERE is_true = 't' AND public.quiz_answers.fk = i_questions[index]);
            END IF;
        END LOOP;
        ret := (correct, answers, correct_answers, correct_answers_id, i_questions, i_answers, question_numbers);
        RETURN ret; 
    END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION private.check_quiz_success(i_questions INT[], i_answers INT[])
    RETURNS RECORD
    AS $$
    DECLARE
        correct BOOLEAN[];
        question_numbers INT[];
        answers TEXT[];
        correct_answers TEXT[];
        correct_answers_id INT[];
        ret RECORD;
    BEGIN
        FOR index IN 1 .. array_upper(i_questions, 1) 
        LOOP
            IF (i_answers[index]) != -1 THEN
                IF (SELECT is_true FROM private.quiz_answers WHERE private.quiz_answers.id = i_answers[index]) THEN
                    correct[index] = 't';
                    answers[index] = (SELECT answer FROM private.quiz_answers WHERE private.quiz_answers.id = i_answers[index]);
                    question_numbers[index] = (SELECT order_number FROM private.quiz_questions WHERE private.quiz_questions.id = i_questions[index]);
                    correct_answers[index] = answers[index];
                    correct_answers_id[index] = (SELECT id FROM private.quiz_answers WHERE is_true = 't' AND private.quiz_answers.fk = i_questions[index]);
                ELSE
                    correct[index] = 'f';
                    answers[index] = (SELECT answer FROM private.quiz_answers WHERE private.quiz_answers.id = i_answers[index]);
                    question_numbers[index] = (SELECT order_number FROM private.quiz_questions WHERE private.quiz_questions.id = i_questions[index]);
                    correct_answers[index] = (SELECT answer FROM private.quiz_answers WHERE is_true = 't' AND private.quiz_answers.fk = i_questions[index]);
                    correct_answers_id[index] = (SELECT id FROM private.quiz_answers WHERE is_true = 't' AND private.quiz_answers.fk = i_questions[index]);
                END IF;
            ELSE
                correct[index] = 'f';
                answers[index] = '';
                question_numbers[index] = (SELECT order_number FROM private.quiz_questions WHERE private.quiz_questions.id = i_questions[index]);
                correct_answers[index] = (SELECT answer FROM private.quiz_answers WHERE is_true = 't' AND private.quiz_answers.fk = i_questions[index]);
                correct_answers_id[index] = (SELECT id FROM private.quiz_answers WHERE is_true = 't' AND private.quiz_answers.fk = i_questions[index]);
            END IF;
        END LOOP;
        ret := (correct, answers, correct_answers, correct_answers_id, i_questions, i_answers, question_numbers);
        RETURN ret; 
    END $$ LANGUAGE plpgsql;
    """)

    
def subscriptions() -> None:
    op.execute("DROP FUNCTION users.add_grade_to_user")
    op.execute("DROP FUNCTION users.add_subject_to_user")
    
    op.execute("""
    CREATE OR REPLACE FUNCTION users.add_grade_to_user(i_user_id int, i_grade_id int, i_subscription_fk int)
    RETURNS TABLE(for_life BOOLEAN, expiration_date TIMESTAMP, plan_name VARCHAR(50))
    AS $$
    DECLARE
        month_count_ INT;
        temprow RECORD;
        i_subject_sub_fk INT;
    BEGIN
        IF (SELECT month_count FROM subscriptions.grade_subscription_plans WHERE id = i_subscription_fk) > 0 THEN
            IF (SELECT users.user_grades.expiration_date FROM users.user_grades WHERE user_fk = i_user_id AND grade_fk = i_grade_id) > now() THEN
                UPDATE users.user_grades SET expiration_date = (SELECT users.user_grades.expiration_date FROM users.user_grades WHERE user_fk = i_user_id AND grade_fk = i_grade_id) + interval '1 month' * (SELECT month_count FROM subscriptions.grade_subscription_plans WHERE id = i_subscription_fk) WHERE user_fk = i_user_id AND grade_fk = i_grade_id;
            ELSE
                INSERT INTO users.user_grades(user_fk, grade_fk, expiration_date, for_life) VALUES (i_user_id, i_grade_id, now() + interval '1 month' * (SELECT month_count FROM subscriptions.grade_subscription_plans WHERE id = i_subscription_fk), 'f');
            END IF;
        ELSE
            INSERT INTO users.user_grades(user_fk, grade_fk, expiration_date, for_life) VALUES (i_user_id, i_grade_id, now(), 't') ON CONFLICT ON CONSTRAINT user_grades_user_fk_grade_fk_key DO UPDATE SET for_life = 't';
        END IF;
        INSERT INTO history.grade_subscriptions(grade_fk, user_fk, price, purchased_at, month_count) VALUES(i_grade_id, i_user_id, (SELECT price FROM subscriptions.grade_subscription_plans WHERE id = i_subscription_fk), now(), (SELECT month_count FROM subscriptions.grade_subscription_plans WHERE id = i_subscription_fk));
        SELECT subscriptions.subject_subscription_plans.id INTO i_subject_sub_fk FROM subscriptions.subject_subscription_plans WHERE month_count = (SELECT month_count FROM subscriptions.grade_subscription_plans WHERE id = i_subscription_fk);
        SELECT month_count INTO month_count_ FROM subscriptions.grade_subscription_plans WHERE id = i_subscription_fk;
        FOR temprow IN
            SELECT id FROM private.subject WHERE private.subject.fk = i_subject_sub_fk
        LOOP
            PERFORM users.add_subject_to_user_by_month_count(i_user_id, temprow.id, month_count_);
        END LOOP;
        RETURN QUERY (SELECT users.user_grades.for_life, users.user_grades.expiration_date, subscriptions.grade_subscription_plans.name FROM users.user_grades INNER JOIN subscriptions.grade_subscription_plans ON id = i_subscription_fk WHERE user_fk = i_user_id AND grade_fk = i_grade_id);
    END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION users.add_subject_to_user_by_month_count(i_user_id int, i_subject_id int, month_count_ int)
    RETURNS VOID
    AS $$
    BEGIN
        IF month_count_ > 0 THEN
            IF (SELECT users.user_subjects.expiration_date FROM users.user_subjects WHERE user_fk = i_user_id AND subject_fk = i_subject_id) > now() THEN
                UPDATE users.user_subjects SET expiration_date = (SELECT users.user_subjects.expiration_date FROM users.user_subjects WHERE user_fk = i_user_id AND subject_fk = i_subject_id) + interval '1 month' * month_count_ WHERE user_fk = i_user_id AND subject_fk = i_subject_id;
            ELSE
                INSERT INTO users.user_subjects(user_fk, subject_fk, expiration_date, for_life) VALUES (i_user_id, i_subject_id, now() + INTERVAL '1 month' * month_count_, 'f');
            END IF;
        ELSE
            INSERT INTO users.user_subjects(user_fk, subject_fk, expiration_date, for_life) VALUES (i_user_id, i_subject_id, now(), 't') ON CONFLICT ON CONSTRAINT user_subjects_user_fk_subject_fk_key DO UPDATE SET for_life = 't';
        END IF;
    END $$ LANGUAGE plpgsql;
    """)

    # add subject to user
    op.execute("""
    CREATE OR REPLACE FUNCTION users.add_subject_to_user(i_user_id int, i_subject_id int, i_subscription_fk int)
    RETURNS TABLE(for_life BOOLEAN, expiration_date TIMESTAMP, plan_name VARCHAR(50))
    AS $$
    BEGIN
        IF (SELECT month_count FROM subscriptions.subject_subscription_plans WHERE id = i_subscription_fk) > 0 THEN
            IF (SELECT users.user_subjects.expiration_date FROM users.user_subjects WHERE user_fk = i_user_id AND subject_fk = i_subject_id) > now() THEN
                UPDATE users.user_subjects SET expiration_date = (SELECT users.user_subjects.expiration_date FROM users.user_subjects WHERE user_fk = i_user_id AND subject_fk = i_subject_id) + interval '1 month' * (SELECT month_count FROM subscriptions.subject_subscription_plans WHERE id = i_subscription_fk) WHERE user_fk = i_user_id AND subject_fk = i_subject_id;
            ELSE
                INSERT INTO users.user_subjects(user_fk, subject_fk, expiration_date, for_life) VALUES (i_user_id, i_subject_id, now() + interval '1 month' * (SELECT month_count FROM subscriptions.subject_subscription_plans WHERE id = i_subscription_fk), 'f');
            END IF;
        ELSE
            INSERT INTO users.user_subjects(user_fk, subject_fk, expiration_date, for_life) VALUES (i_user_id, i_subject_id, now(), 't') ON CONFLICT ON CONSTRAINT user_subjects_user_fk_subject_fk_key DO UPDATE SET for_life = 't';
        END IF;
        INSERT INTO history.subject_subscriptions(subject_fk, user_fk, price, purchased_at, month_count) VALUES(i_subject_id, i_user_id, (SELECT price FROM subscriptions.subject_subscription_plans WHERE id = i_subscription_fk), now(), (SELECT month_count FROM subscriptions.subject_subscription_plans WHERE id = i_subscription_fk));
        RETURN QUERY (SELECT users.user_subjects.for_life, users.user_subjects.expiration_date, subscriptions.subject_subscription_plans.name FROM users.user_subjects INNER JOIN subscriptions.subject_subscription_plans ON id = i_subscription_fk WHERE user_fk = i_user_id AND subject_fk = i_subject_id);
    END $$ LANGUAGE plpgsql;
    """)


def front_page_titles() -> None:
    op.create_table('titles',
    sa.Column('main_title', sa.Text, nullable=True),
    sa.Column('example_title', sa.Text, nullable=True),
    sa.Column('subscription_instruction_title', sa.Text, nullable=True),
    sa.Column('questions_title', sa.Text, nullable=True),
    sa.Column('questions_sub_title', sa.Text, nullable=True),
    schema='public'
    )

    op.execute("""
    CREATE OR REPLACE FUNCTION public.insert_title(main_title_ TEXT, example_title_ TEXT, subscription_instruction_title_ TEXT, questions_title_ TEXT, questions_sub_title_ TEXT)
    RETURNS TABLE(main_title TEXT, example_title TEXT, subscription_instruction_title TEXT, questions_title TEXT, questions_sub_title TEXT)
    AS $$
    BEGIN
        IF (SELECT COUNT(*) FROM public.titles) > 0 THEN
            UPDATE public.titles SET
                main_title = COALESCE(main_title_, public.titles.main_title),
                example_title = COALESCE(example_title_, public.titles.example_title),
                subscription_instruction_title = COALESCE(subscription_instruction_title_, public.titles.subscription_instruction_title),
                questions_title = COALESCE(questions_title_, public.titles.questions_title),
                questions_sub_title = COALESCE(questions_sub_title_, public.titles.questions_sub_title);
        ELSE
            INSERT INTO public.titles(main_title, example_title, subscription_instruction_title, questions_title, questions_sub_title)
            VALUES(main_title_, example_title_, subscription_instruction_title_, questions_title_, questions_sub_title_);
        END IF; 
        RETURN QUERY(SELECT t.main_title, t.example_title, t.subscription_instruction_title, t.questions_title, t.questions_sub_title FROM public.titles AS t);
    END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION public.get_front_page_titles()
    RETURNS TABLE(main_title TEXT, example_title TEXT, subscription_instruction_title TEXT, questions_title TEXT, questions_sub_title TEXT)
    AS $$
    BEGIN
        RETURN QUERY(SELECT t.main_title, t.example_title, t.subscription_instruction_title, t.questions_title, t.questions_sub_title FROM public.titles AS t);
    END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION public.delete_main_title()
    RETURNS VOID
    AS $$
    BEGIN 
        UPDATE public.titles SET main_title = NULL;
    END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION public.delete_example_title()
    RETURNS VOID
    AS $$
    BEGIN 
        UPDATE public.titles SET example_title = NULL;
    END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION public.delete_subscriptions_title()
    RETURNS VOID
    AS $$
    BEGIN 
        UPDATE public.titles SET subscription_instruction_title = NULL;
    END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION public.delete_questions_title()
    RETURNS VOID
    AS $$
    BEGIN 
        UPDATE public.titles SET questions_title = NULL;
    END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION public.delete_questions_sub_title()
    RETURNS VOID
    AS $$
    BEGIN 
        UPDATE public.titles SET questions_sub_title = NULL;
    END $$ LANGUAGE plpgsql;
    """)

def active_subscriptions() -> None:
    op.execute("""
    CREATE OR REPLACE FUNCTION subscriptions.get_subject_subscriptions(user_id INT)
    RETURNS TABLE(class_name VARCHAR(100), subject_name VARCHAR(100), expiration_date TIMESTAMP, for_life BOOLEAN)
    AS $$
    BEGIN
        RETURN QUERY(SELECT c.name_ru, s.name_ru, u.expiration_date, u.for_life FROM users.user_subjects AS u 
        INNER JOIN private.subject AS s ON s.id = u.subject_fk 
        INNER JOIN private.grade AS c ON c.id = s.fk 
        WHERE user_fk = user_id);
    END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION subscriptions.get_grade_subscriptions(user_id INT)
    RETURNS TABLE(class_name VARCHAR(100), expiration_date TIMESTAMP, for_life BOOLEAN)
    AS $$
    BEGIN
        RETURN QUERY(SELECT c.name_ru, u.expiration_date, u.for_life FROM users.user_grades AS u 
        INNER JOIN private.grade AS c ON c.id = u.grade_fk
        WHERE user_fk = user_id);
    END $$ LANGUAGE plpgsql;
    """)

def drop_front_page_functions() -> None:
    functions = [
        'insert_title',
        'get_front_page_titles',
        'delete_main_title',
        'delete_example_title',
        'delete_subscriptions_title',
        'delete_questions_title',
        'delete_questions_sub_title',
    ]

    for function in functions:
        op.execute(f"DROP FUNCTION public.{function}")


def drop_active_subscriptions_functions() -> None:
    functions = [
        'get_subject_subscriptions',
        'get_grade_subscriptions',
    ]

    for function in functions:
        op.execute(f"DROP FUNCTION subscriptions.{function}")


def upgrade() -> None:
    quiz()
    subscriptions()
    front_page_titles()
    active_subscriptions()

def downgrade() -> None:
    op.execute("DROP FUNCTION users.add_subject_to_user_by_month_count")
    drop_front_page_functions()
    op.execute("DROP TABLE public.titles")
    drop_active_subscriptions_functions()
