"""quiz
Revision ID: 000fc98ce9cf
Revises: 242510e32be9
Create Date: 2021-06-27 12:56:19.903230
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '000fc98ce9cf'
down_revision = '242510e32be9'
branch_labels = None
depends_on = None

def create_unique_index() -> None:
    # create unique index for table quiz_answers
    # there can be many answer options for one question
    # but only one of them can be true
    op.execute("CREATE UNIQUE INDEX only_one_row_with_column_true_uix ON private.quiz_answers (fk, is_true) WHERE (is_true)") 

def create_tables() -> None:
    # question tables
    op.create_table(
        "quiz_questions",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("fk", sa.Integer, nullable=False),
        sa.Column("order_number", sa.Integer, nullable=False),
        sa.Column("question", sa.Text, nullable=True),
        sa.Column("image_key", sa.Text, nullable=True),
        sa.Column("image_url", sa.Text, nullable=True),
        sa.ForeignKeyConstraint(['fk'], ['private.lecture.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.UniqueConstraint('fk', 'order_number'),
        schema='private'
    )
    # answers tables
    op.create_table(
        "quiz_answers",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("fk", sa.Integer, nullable=False),
        sa.Column("answer", sa.Text, nullable=False),
        sa.Column("is_true", sa.Boolean, nullable=True),
        sa.ForeignKeyConstraint(['fk'], ['private.quiz_questions.id'], onupdate="CASCADE", ondelete='CASCADE'),
        schema='private'
    )
    # add unique constraint to quiz answers
    create_unique_index()

def drop_tables() -> None:
    op.execute("DROP TABLE private.quiz_answers")
    op.execute("DROP TABLE private.quiz_questions")

def create_quiz_handling_functions() -> None:
    # insert question
    op.execute("""
    CREATE OR REPLACE FUNCTION private.insert_quiz_question(i_lecture_id int, i_order_number int, i_question text, i_image_key text, i_image_url text, i_answers text[], i_is_true boolean[])
    RETURNS TABLE (id int, fk int, order_number int, question text, image_key text, image_url text, answer_id int, question_id int, answer text, is_true boolean)
    AS $$
    DECLARE 
        inserted int;
    BEGIN
        INSERT INTO private.quiz_questions(fk, order_number, question, image_key, image_url) VALUES (i_lecture_id, i_order_number, i_question ,i_image_key, i_image_url) RETURNING private.quiz_questions.id INTO inserted;
        FOR index IN 1 .. array_upper(i_answers, 1)
        LOOP
            INSERT INTO private.quiz_answers(fk, answer, is_true) VALUES(inserted, i_answers[index], i_is_true[index]);
        END LOOP;
        RETURN QUERY (SELECT * FROM private.quiz_questions INNER JOIN private.quiz_answers AS qa ON private.quiz_questions.id = qa.fk WHERE private.quiz_questions.id = inserted);
    END $$ LANGUAGE plpgsql;
    """)
    # insert answers to question
    op.execute("""
    CREATE OR REPLACE FUNCTION private.insert_quiz_answers(i_question_id int, i_answer text[], i_is_true boolean[])
    RETURNS TABLE (answer_id int, question_id int, answer text, is_true boolean)
    AS $$
    BEGIN
        FOR index IN 1 .. array_upper(i_answer, 1)
        LOOP
            INSERT INTO private.quiz_answers(fk, answer, is_true) VALUES(i_question_id, i_answer[index], i_is_true[index]);
        END LOOP;
        RETURN QUERY (SELECT id AS answer_id, fk AS question_id, private.quiz_answers.answer, private.quiz_answers.is_true FROM private.quiz_answers WHERE private.quiz_answers.fk = i_question_id);
    END $$ LANGUAGE plpgsql;
    """)
    # select questions by lecture
    op.execute("""
    CREATE OR REPLACE FUNCTION private.get_quiz_questions(i_lecture_id int)
    RETURNS TABLE (id int, fk int, order_number int, question text, image_key text, image_url text)
    AS $$
    BEGIN
        RETURN QUERY (SELECT * FROM private.quiz_questions WHERE private.quiz_questions.fk = i_lecture_id ORDER BY private.quiz_questions.order_number);
    END $$ LANGUAGE plpgsql;
    """)
    # select answers by questions
    op.execute("""
    CREATE OR REPLACE FUNCTION private.get_quiz_answers(i_question_id int)
    RETURNS TABLE (question_id int, answer_id int, answer text, is_true boolean)
    AS $$
    BEGIN
        RETURN QUERY (SELECT qa.fk, qa.id, qa.answer, qa.is_true FROM private.quiz_answers AS qa WHERE qa.fk = i_question_id);
    END $$ LANGUAGE plpgsql;
    """)

    # delete question
    op.execute("""
    CREATE OR REPLACE FUNCTION private.delete_quiz_by_id(i_question_id int)
    RETURNS text
    AS $$
    DECLARE 
        key text;
    BEGIN
        DELETE FROM private.quiz_questions WHERE id = i_question_id RETURNING image_key INTO key;
        RETURN key;
    END $$ LANGUAGE plpgsql;
    """)

    # select all keys for updating image links
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_all_quiz_question_keys()
    RETURNS TABLE (id int, key text)
    AS $$
    BEGIN
        RETURN QUERY (SELECT private.quiz_questions.id, image_key FROM private.quiz_questions);
    END $$ LANGUAGE plpgsql;
    """)
    # update all links by keys
    op.execute("""
    CREATE OR REPLACE FUNCTION private.update_quiz_links(keys text[], urls text[])
    RETURNS VOID
    AS $$
    BEGIN
        FOR index IN 1 .. array_upper(keys, 1)
        LOOP
            UPDATE private.quiz_questions SET
                image_url = urls[index]
            WHERE image_key = keys[index];
        END LOOP;
    END $$ LANGUAGE plpgsql;
    """)

    # check test
    op.execute("""
    CREATE OR REPLACE FUNCTION private.check_quiz_success(i_questions INT[], i_answers INT[])
    RETURNS RECORD
    AS $$
    DECLARE
        correct BOOLEAN[];
        question_numbers INT[];
        answers TEXT[];
        correct_answers TEXT[];
        ret RECORD;
    BEGIN
        FOR index IN 1 .. array_upper(i_questions, 1) 
        LOOP
            IF (SELECT is_true FROM private.quiz_answers WHERE private.quiz_answers.id = i_answers[index]) THEN
                correct[index] = 't';
                answers[index] = (SELECT answer FROM private.quiz_answers WHERE private.quiz_answers.id = i_answers[index]);
                question_numbers[index] = (SELECT order_number FROM private.quiz_questions WHERE private.quiz_questions.id = i_questions[index]);
                correct_answers[index] = answers[index];
            ELSE
                correct[index] = 'f';
                answers[index] = (SELECT answer FROM private.quiz_answers WHERE private.quiz_answers.id = i_answers[index]);
                question_numbers[index] = (SELECT order_number FROM private.quiz_questions WHERE private.quiz_questions.id = i_questions[index]);
                correct_answers[index] = (SELECT answer FROM private.quiz_answers WHERE is_true = 't' AND private.quiz_answers.fk = i_questions[index]);
            END IF;
        END LOOP;
        ret := (correct, answers, correct_answers, i_questions, i_answers, question_numbers);
        RETURN ret; 
    END $$ LANGUAGE plpgsql;
    """)

def drop_quiz_handling_functions() -> None:
    functions = [
        'insert_quiz_question',
        'insert_quiz_answers',
        'get_quiz_questions',
        'get_quiz_answers',
        'select_all_quiz_question_keys',
        'update_quiz_links',
        'delete_quiz_by_id',
        'check_quiz_success'
    ]

    for function in functions:
        op.execute(f"DROP FUNCTION private.{function} CASCADE")

def upgrade() -> None:
    create_tables()
    create_quiz_handling_functions()

def downgrade() -> None:
    drop_tables()
    drop_quiz_handling_functions()