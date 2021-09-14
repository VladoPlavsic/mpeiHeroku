"""public stored procedures
Revision ID: 124a05dc847d
Revises: 6e7bb8073b9f
Create Date: 2021-03-31 08:36:12.946707
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '124a05dc847d'
down_revision = '6e7bb8073b9f'
branch_labels = None
depends_on = None

def create_insert_public_procedures() -> None:
    # game
    op.execute("""
    CREATE OR REPLACE FUNCTION public.insert_game(varchar(100), text, text, text)
        RETURNS TABLE (name_ru varchar(100), url text, description text, object_key text)
        AS $$
        BEGIN
        DELETE FROM public.game;
        INSERT INTO public.game (name_ru, url, description, object_key) VALUES ($1, $2, $3, $4);
        RETURN QUERY (SELECT * FROM public.game);
        END $$ LANGUAGE plpgsql;
    """)
    # video
    op.execute("""
    CREATE OR REPLACE FUNCTION public.insert_video(varchar(100), text, text, text)
        RETURNS TABLE (name_ru varchar(100), url text, description text, object_key text)
        AS $$
        BEGIN
        DELETE FROM public.video;
        INSERT INTO public.video (name_ru, url, description, object_key) VALUES ($1, $2, $3, $4);
        RETURN QUERY (SELECT * FROM public.video);
        END $$ LANGUAGE plpgsql;
    """)
    # book
    op.execute("""
    CREATE OR REPLACE FUNCTION public.insert_book(varchar(100), text, text, text)
        RETURNS TABLE (name_ru varchar(100), url text, description text, object_key text)
        AS $$
        BEGIN
        DELETE FROM public.book;
        INSERT INTO public.book (name_ru, url, description, object_key) VALUES ($1, $2, $3, $4);
        RETURN QUERY (SELECT * FROM public.book);
        END $$ LANGUAGE plpgsql;
    """)
    # practice
    op.execute("""
    CREATE OR REPLACE FUNCTION public.insert_practice(varchar(100), text, text)
        RETURNS TABLE (name_ru varchar(100), description text, object_key text)
        AS $$
        BEGIN
        DELETE FROM public.practice;
        INSERT INTO public.practice (name_ru, description, object_key) VALUES ($1, $2, $3);
        RETURN QUERY (SELECT * FROM public.practice);
        END $$ LANGUAGE plpgsql;
    """)
    # theory
    op.execute("""
    CREATE OR REPLACE FUNCTION public.insert_theory(varchar(100), text, text)
        RETURNS TABLE (name_ru varchar(100), description text, object_key text)
        AS $$
        BEGIN
        DELETE FROM public.theory;
        INSERT INTO public.theory (name_ru, description, object_key) VALUES ($1, $2, $3);
        RETURN QUERY (SELECT * FROM public.theory);
        END $$ LANGUAGE plpgsql;
    """)

     # theory images insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION public.insert_theory_image(int[], text[], text[])
        RETURNS TABLE ("order" int, url text, object_key text)
        AS $$
        BEGIN
        DELETE FROM public.theory_image;
        INSERT INTO public.theory_image ("order", url, object_key)
        SELECT unnest($1), unnest($2), unnest($3);
        RETURN QUERY (SELECT public.theory_image."order", public.theory_image.url, public.theory_image.object_key FROM public.theory_image);
        END $$ LANGUAGE plpgsql;
    """)

    # theory audio insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION public.insert_theory_audio(int[], text[], text[])
        RETURNS TABLE ("order" int, url text, object_key text)
        AS $$
        BEGIN
        DELETE FROM public.theory_audio;
        INSERT INTO public.theory_audio ("order", url, object_key)
        SELECT unnest($1), unnest($2), unnest($3);
        RETURN QUERY (SELECT public.theory_audio."order", public.theory_audio.url, public.theory_audio.object_key FROM public.theory_audio);
        END $$ LANGUAGE plpgsql;
    """)

    # practice images insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION public.insert_practice_image(int[], text[], text[])
        RETURNS TABLE ("order" int, url text, object_key text)
        AS $$
        BEGIN
        DELETE FROM public.practice_image;
        INSERT INTO public.practice_image ("order", url, object_key)
        SELECT unnest($1), unnest($2), unnest($3);
        RETURN QUERY (SELECT public.practice_image."order", public.practice_image.url, public.practice_image.object_key FROM public.practice_image);
        END $$ LANGUAGE plpgsql;
    """)
    # practice audio insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION public.insert_practice_audio(int[], text[], text[])
        RETURNS TABLE ("order" int, url text, object_key text)
        AS $$
        BEGIN
        DELETE FROM public.practice_audio;
        INSERT INTO public.practice_audio ("order", url, object_key)
        SELECT unnest($1), unnest($2), unnest($3);
        RETURN QUERY (SELECT public.practice_audio."order", public.practice_audio.url, public.practice_audio.object_key FROM public.practice_audio);
        END $$ LANGUAGE plpgsql;
    """)

    # about us insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION public.insert_about_us(int, text, text, text)
        RETURNS TABLE ("order" int, title text, description text, svg text)
        AS $$
        DECLARE
            inserted_id int;
        BEGIN
        INSERT INTO public.about_us ("order", title, description, svg) VALUES ($1, $2, $3, $4) RETURNING public.about_us.order INTO inserted_id;
        RETURN QUERY (SELECT * FROM public.about_us WHERE public.about_us.order = inserted_id);
        END $$ LANGUAGE plpgsql;
    """)
    # faq insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION public.insert_faq(text, text)
        RETURNS TABLE (id int, question text, answer text)
        AS $$
        DECLARE
            inserted_id int;
        BEGIN
        INSERT INTO public.faq (question, answer) VALUES ($1, $2) RETURNING public.faq.id INTO inserted_id;
        RETURN QUERY (SELECT * FROM public.faq WHERE public.faq.id = inserted_id);
        END $$ LANGUAGE plpgsql;
    """)
    # instruction insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION public.insert_instruction(int, text, text)
        RETURNS TABLE ("order" int, title text, description text)
        AS $$
        DECLARE
            inserted_id int;
        BEGIN
        INSERT INTO public.instruction ("order", title, description) VALUES ($1, $2, $3) RETURNING public.instruction.order INTO inserted_id;
        RETURN QUERY (SELECT * FROM public.instruction WHERE public.instruction.order = inserted_id);
        END $$ LANGUAGE plpgsql;
    """)

def create_select_public_procedures() -> None:
    # video
    op.execute("""
    CREATE OR REPLACE FUNCTION public.select_video()
        RETURNS TABLE (url text, name_ru varchar(20), description text, object_key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT public.video.url, public.video.name_ru, public.video.description, public.video.object_key FROM public.video);
        END $$ LANGUAGE plpgsql;
    """)
    
    # book
    op.execute("""
    CREATE OR REPLACE FUNCTION public.select_book()
        RETURNS TABLE (url text, name_ru varchar(20), description text, object_key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT public.book.url, public.book.name_ru, public.book.description, public.book.object_key FROM public.book);
        END $$ LANGUAGE plpgsql;
    """)

    # game
    op.execute("""
    CREATE OR REPLACE FUNCTION public.select_game()
        RETURNS TABLE (url text, name_ru varchar(20), description text, object_key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT public.game.url, public.game.name_ru, public.game.description, public.game.object_key FROM public.game);
        END $$ LANGUAGE plpgsql;
    """)

    # theory
    op.execute("""
    CREATE OR REPLACE FUNCTION public.select_theory()
        RETURNS TABLE (name_ru varchar(20), description text, object_key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT public.theory.name_ru, public.theory.description, public.theory.object_key FROM public.theory);
        END $$ LANGUAGE plpgsql;
    """)
    # thoery images
    op.execute("""
    CREATE OR REPLACE FUNCTION public.select_theory_image()
        RETURNS TABLE (url text, "order" int, object_key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT public.theory_image.url, public.theory_image."order", public.theory_image.object_key FROM public.theory_image ORDER BY public.theory_image.order);
        END $$ LANGUAGE plpgsql;
    """)
    # theory audio
    op.execute("""
    CREATE OR REPLACE FUNCTION public.select_theory_audio()
        RETURNS TABLE (url text, "order" int, object_key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT public.theory_audio.url, public.theory_audio."order", public.theory_audio.object_key FROM public.theory_audio ORDER BY public.theory_audio.order);
        END $$ LANGUAGE plpgsql;
    """)
    
    # practice
    op.execute("""
    CREATE OR REPLACE FUNCTION public.select_practice()
        RETURNS TABLE (name_ru varchar(20), description text, object_key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT public.practice.name_ru, public.practice.description, public.practice.object_key FROM public.practice);
        END $$ LANGUAGE plpgsql;
    """)
    # practice images
    op.execute("""
    CREATE OR REPLACE FUNCTION public.select_practice_image()
        RETURNS TABLE (url text, "order" int, object_key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT public.practice_image.url, public.practice_image."order", public.practice_image.object_key FROM public.practice_image ORDER BY public.practice_image.order);
        END $$ LANGUAGE plpgsql;
    """)
    # practice audio
    op.execute("""
    CREATE OR REPLACE FUNCTION public.select_practice_audio()
        RETURNS TABLE (url text, "order" int, object_key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT public.practice_audio.url, public.practice_audio."order", public.practice_audio.object_key FROM public.practice_audio ORDER BY public.practice_audio.order);
        END $$ LANGUAGE plpgsql;
    """)

    # AboutUs, Instruction, FAQ
    op.execute("""
    CREATE OR REPLACE FUNCTION public.select_about_us()
        RETURNS TABLE ("order" int, title text, description text, svg text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT public.about_us.order, public.about_us.title, public.about_us.description, public.about_us.svg FROM public.about_us ORDER BY public.about_us.order);
        END $$ LANGUAGE plpgsql;
    """)
    # instruction
    op.execute("""
    CREATE OR REPLACE FUNCTION public.select_instruction()
        RETURNS TABLE ("order" int, title text, description text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT public.instruction.order, public.instruction.title, public.instruction.description FROM public.instruction ORDER BY public.instruction.order);
        END $$ LANGUAGE plpgsql;
    """)
    # faq
    op.execute("""
    CREATE OR REPLACE FUNCTION public.select_faq(int, int)
        RETURNS TABLE (id int, question text, answer text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT public.faq.id, public.faq.question, public.faq.answer FROM public.faq WHERE public.faq.id > $1 LIMIT $2);
        END $$ LANGUAGE plpgsql;
    """)

def create_quiz_handling_functions() -> None:
    # insert question
    op.execute("""
    CREATE OR REPLACE FUNCTION public.insert_quiz_question(i_order_number int, i_question text, i_object_key text, i_image_url text, i_answers text[], i_is_true boolean[])
    RETURNS TABLE (id int, order_number int, question text, object_key text, image_url text, answer_id int, question_id int, answer text, is_true boolean)
    AS $$
    DECLARE 
        inserted int;
    BEGIN
        INSERT INTO public.quiz_questions(order_number, question, object_key, image_url) VALUES (i_order_number, i_question ,i_object_key, i_image_url) RETURNING public.quiz_questions.id INTO inserted;
        FOR index IN 1 .. array_upper(i_answers, 1)
        LOOP
            INSERT INTO public.quiz_answers(fk, answer, is_true) VALUES(inserted, i_answers[index], i_is_true[index]);
        END LOOP;
        RETURN QUERY (SELECT * FROM public.quiz_questions INNER JOIN public.quiz_answers AS qa ON public.quiz_questions.id = qa.fk WHERE public.quiz_questions.id = inserted);
    END $$ LANGUAGE plpgsql;
    """)
    # insert answers to question
    op.execute("""
    CREATE OR REPLACE FUNCTION public.insert_quiz_answers(i_question_id int, i_answer text[], i_is_true boolean[])
    RETURNS TABLE (answer_id int, question_id int, answer text, is_true boolean)
    AS $$
    BEGIN
        FOR index IN 1 .. array_upper(i_answer, 1)
        LOOP
            INSERT INTO public.quiz_answers(fk, answer, is_true) VALUES(i_question_id, i_answer[index], i_is_true[index]);
        END LOOP;
        RETURN QUERY (SELECT id AS answer_id, fk AS question_id, public.quiz_answers.answer, public.quiz_answers.is_true FROM public.quiz_answers WHERE public.quiz_answers.fk = i_question_id);
    END $$ LANGUAGE plpgsql;
    """)
    # select questions
    op.execute("""
    CREATE OR REPLACE FUNCTION public.get_quiz_questions()
    RETURNS TABLE (id int, order_number int, question text, object_key text, image_url text)
    AS $$
    BEGIN
        RETURN QUERY (SELECT * FROM public.quiz_questions ORDER BY public.quiz_questions.order_number);
    END $$ LANGUAGE plpgsql;
    """)
    # select answers by questions
    op.execute("""
    CREATE OR REPLACE FUNCTION public.get_quiz_answers(i_question_id int)
    RETURNS TABLE (question_id int, answer_id int, answer text, is_true boolean)
    AS $$
    BEGIN
        RETURN QUERY (SELECT qa.fk, qa.id, qa.answer, qa.is_true FROM public.quiz_answers AS qa WHERE qa.fk = i_question_id);
    END $$ LANGUAGE plpgsql;
    """)

    # delete question
    op.execute("""
    CREATE OR REPLACE FUNCTION public.delete_quiz_by_id(i_question_id int)
    RETURNS text
    AS $$
    DECLARE 
        key text;
    BEGIN
        DELETE FROM public.quiz_questions WHERE id = i_question_id RETURNING object_key INTO key;
        RETURN key;
    END $$ LANGUAGE plpgsql;
    """)
    
    # delete whole quiz 
    op.execute("""
    CREATE OR REPLACE FUNCTION public.delete_all_quiz()
    RETURNS setof TEXT
    AS $$
        DELETE FROM public.quiz_questions RETURNING public.quiz_questions.object_key;
    $$ LANGUAGE sql;
    """)

    # select all keys for updating image links
    op.execute("""
    CREATE OR REPLACE FUNCTION public.select_all_quiz_question_keys()
    RETURNS TABLE (object_key text)
    AS $$
    BEGIN
        RETURN QUERY (SELECT public.quiz_questions.object_key FROM public.quiz_questions);
    END $$ LANGUAGE plpgsql;
    """)
    # update all links by keys
    op.execute("""
    CREATE OR REPLACE FUNCTION public.update_quiz_links(keys text[], urls text[])
    RETURNS VOID
    AS $$
    BEGIN
        FOR index IN 1 .. array_upper(keys, 1)
        LOOP
            UPDATE public.quiz_questions SET
                image_url = urls[index]
            WHERE object_key = keys[index];
        END LOOP;
    END $$ LANGUAGE plpgsql;
    """)

    # check test
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
        END LOOP;
        ret := (correct, answers, correct_answers, correct_answers_id, i_questions, i_answers, question_numbers);
        RETURN ret; 
    END $$ LANGUAGE plpgsql;
    """)


def create_update_public_procedures() -> None:
    # video
    op.execute("""
    CREATE OR REPLACE FUNCTION public.update_video(varchar(100), text)
        RETURNS TABLE (name_ru varchar(100), url text, description text, object_key text)
        AS $$
        BEGIN
        UPDATE public.video SET
            name_ru = COALESCE($1, public.video.name_ru),
            description = COALESCE($2, public.video.description);
        RETURN QUERY (SELECT * FROM public.video);
        END $$ LANGUAGE plpgsql;
    """)
    # game
    op.execute("""
    CREATE OR REPLACE FUNCTION public.update_game(varchar(100), text)
        RETURNS TABLE (name_ru varchar(100), url text, description text, object_key text)
        AS $$
        BEGIN
        UPDATE public.game SET
            name_ru = COALESCE($1, public.game.name_ru),
            description = COALESCE($2, public.game.description);
        RETURN QUERY (SELECT * FROM public.game);
        END $$ LANGUAGE plpgsql;
    """)
    # book
    op.execute("""
    CREATE OR REPLACE FUNCTION public.update_book(varchar(100), text)
        RETURNS TABLE (name_ru varchar(100), url text, description text, object_key text)
        AS $$
        BEGIN
        UPDATE public.book SET
            name_ru = COALESCE($1, public.book.name_ru),
            description = COALESCE($2, public.book.description);
        RETURN QUERY (SELECT * FROM public.book);
        END $$ LANGUAGE plpgsql;
    """)
    # theory
    op.execute("""
    CREATE OR REPLACE FUNCTION public.update_theory_metadata(varchar(100), text)
        RETURNS TABLE (name_ru varchar(100), description text, object_key text)
        AS $$
        BEGIN
        UPDATE public.theory SET
            name_ru = COALESCE($1, public.theory.name_ru),
            description = COALESCE($2, public.theory.description);
        RETURN QUERY (SELECT * FROM public.theory);
        END $$ LANGUAGE plpgsql;
    """)
    # practice
    op.execute("""
    CREATE OR REPLACE FUNCTION public.update_practice_metadata(varchar(100), text)
        RETURNS TABLE (name_ru varchar(100), description text, object_key text)
        AS $$
        BEGIN
        UPDATE public.practice SET
            name_ru = COALESCE($1, public.practice.name_ru),
            description = COALESCE($2, public.practice.description);
        RETURN QUERY (SELECT * FROM public.practice);
        END $$ LANGUAGE plpgsql;
    """)
    
    # about_us
    op.execute("""
    CREATE OR REPLACE FUNCTION public.update_about_us(int, text, text, text)
        RETURNS TABLE ("order" int, title text, description text, svg text)
        AS $$
        BEGIN
        UPDATE public.about_us SET
            title = COALESCE($2, public.about_us.title),
            description = COALESCE($3, public.about_us.description),
            svg = COALESCE($4, public.about_us.svg)
        WHERE public.about_us.order = $1; 
        RETURN QUERY (SELECT public.about_us.order, public.about_us.title, public.about_us.description, public.about_us.svg FROM public.about_us WHERE public.about_us.order = $1);
        END $$ LANGUAGE plpgsql;
    """)
    # instruction
    op.execute("""
    CREATE OR REPLACE FUNCTION public.update_instruction(int, text, text)
        RETURNS TABLE ("order" int, title text, description text)
        AS $$
        BEGIN
        UPDATE public.instruction SET
            title = COALESCE($2, public.instruction.title),
            description = COALESCE($3, public.instruction.description)
        WHERE public.instruction.order = $1; 
        RETURN QUERY (SELECT public.instruction.order, public.instruction.title, public.instruction.description FROM public.instruction WHERE public.instruction.order = $1);
        END $$ LANGUAGE plpgsql;
    """)
    # faq
    op.execute("""
    CREATE OR REPLACE FUNCTION public.update_faq(int, text, text)
        RETURNS TABLE (id int, question text, answer text)
        AS $$
        BEGIN
        UPDATE public.faq SET
            question = COALESCE($2, public.faq.question),
            answer = COALESCE($3, public.faq.answer)
        WHERE public.faq.id = $1; 
        RETURN QUERY (SELECT public.faq.id, public.faq.question, public.faq.answer FROM public.faq WHERE public.faq.id = $1);
        END $$ LANGUAGE plpgsql;
    """)
    

def create_delete_public_procedures() -> None:
    # video
    op.execute("""
    CREATE OR REPLACE FUNCTION public.delete_video()
        RETURNS TEXT
        AS $$
        DECLARE
            key text;
        BEGIN 
            DELETE FROM public.video RETURNING public.video.object_key INTO key;
        RETURN key;
        END $$ LANGUAGE plpgsql;
    """)
    # game
    op.execute("""
    CREATE OR REPLACE FUNCTION public.delete_game()
        RETURNS TEXT
        AS $$
        DECLARE 
            key text;
        BEGIN 
            DELETE FROM public.game RETURNING public.game.object_key INTO key;
        RETURN key;
        END $$ LANGUAGE plpgsql;
    """)
    # book
    op.execute("""
    CREATE OR REPLACE FUNCTION public.delete_book()
        RETURNS text
        AS $$
        DECLARE
            key text;
        BEGIN 
            DELETE FROM public.book RETURNING public.book.object_key INTO key;
        RETURN key;
        END $$ LANGUAGE plpgsql;
    """)
    # theory
    op.execute("""
    CREATE OR REPLACE FUNCTION public.delete_theory()
        RETURNS text
        AS $$
        DECLARE 
            key text;
        BEGIN
            DELETE FROM public.theory RETURNING public.theory.object_key INTO key;
            DELETE FROM public.theory_image;
            DELETE FROM public.theory_audio;
        RETURN key;
        END $$ LANGUAGE plpgsql;
    """)
    # practice
    op.execute("""
    CREATE OR REPLACE FUNCTION public.delete_practice()
        RETURNS text
        AS $$
        DECLARE
            key text;
        BEGIN 
            DELETE FROM public.practice RETURNING public.practice.object_key INTO key;
            DELETE FROM public.practice_image;
            DELETE FROM public.practice_audio;
        RETURN key;
        END $$ LANGUAGE plpgsql;
    """)
    
    # about us
    op.execute("""
    CREATE OR REPLACE FUNCTION public.delete_about_us(int)
        RETURNS VOID
        AS $$
        BEGIN 
        DELETE FROM public.about_us WHERE public.about_us.order = $1;
        END $$ LANGUAGE plpgsql;
    """)
    # faq
    op.execute("""
    CREATE OR REPLACE FUNCTION public.delete_faq(int)
        RETURNS VOID
        AS $$
        BEGIN 
        DELETE FROM public.faq WHERE public.faq.id = $1;
        END $$ LANGUAGE plpgsql;
    """)
    # instruction
    op.execute("""
    CREATE OR REPLACE FUNCTION public.delete_instruction(int)
        RETURNS VOID
        AS $$
        BEGIN 
        DELETE FROM public.instruction WHERE public.instruction.order = $1;
        END $$ LANGUAGE plpgsql;
    """)
    
def create_on_delete_triggers() -> None:
    # update all order numbers to shift left after deleting about us and instruction

    # updating about us order number function
    op.execute("""
    CREATE OR REPLACE FUNCTION public.update_about_us_order_numbers_after_delete() RETURNS trigger
    AS $$
    DECLARE 
        temprow RECORD;
        order_num int;
    BEGIN
        order_num = OLD.order;
        FOR temprow IN 
                SELECT "order" FROM public.about_us WHERE public.about_us.order > OLD.order ORDER BY public.about_us.order
            LOOP
                UPDATE public.about_us SET
                    "order" = order_num
                WHERE "order" = temprow.order;
                order_num = order_num + 1;
            END LOOP;
            RETURN NULL;
    END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE TRIGGER update_about_us_order_numbers_after_delete_trigger AFTER DELETE ON public.about_us 
    FOR EACH ROW EXECUTE PROCEDURE public.update_about_us_order_numbers_after_delete();
    """)

    # updating instruction order number function
    op.execute("""
    CREATE OR REPLACE FUNCTION public.update_instruction_order_numbers_after_delete() RETURNS trigger
    AS $$
    DECLARE 
        temprow RECORD;
        order_num int;
    BEGIN
        order_num = OLD.order;
        FOR temprow IN 
                SELECT "order" FROM public.instruction WHERE public.instruction.order > OLD.order ORDER BY public.instruction.order
            LOOP
                UPDATE public.instruction SET
                    "order" = order_num
                WHERE "order" = temprow.order;
                order_num = order_num + 1;
            END LOOP;
            RETURN NULL;
    END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE TRIGGER update_instruction_order_numbers_after_delete_trigger AFTER DELETE ON public.instruction 
    FOR EACH ROW EXECUTE PROCEDURE public.update_instruction_order_numbers_after_delete();
    """)

def drop_public_procedures() -> None:
    procedures = [
        'insert_practice_audio',
        'insert_practice_image',
        'insert_theory_audio',
        'insert_theory_image',
        'insert_theory',
        'insert_practice',
        'insert_book',
        'insert_video',
        'insert_game',
        'insert_about_us',
        'insert_faq',
        'insert_instruction',
        'select_video',
        'select_book',
        'select_game',
        'select_theory',
        'select_theory_image',
        'select_theory_audio',
        'select_practice',
        'select_practice_image',
        'select_practice_audio',
        'select_faq',
        'select_instruction',
        'select_about_us',
        'update_video',
        'update_game',
        'update_book',
        'update_theory_metadata',
        'update_practice_metadata',
        'update_about_us',
        'update_faq',
        'update_instruction',
        'delete_video',
        'delete_book',
        'delete_game',
        'delete_theory',
        'delete_practice',
        'delete_about_us',
        'delete_faq',
        'delete_instruction',
        'update_about_us_order_numbers_after_delete',
        'update_instruction_order_numbers_after_delete',
        'insert_quiz_question',
        'insert_quiz_answers',
        'get_quiz_questions',
        'get_quiz_answers',
        'select_all_quiz_question_keys',
        'update_quiz_links',
        'delete_quiz_by_id',
        'check_quiz_success',
        'delete_all_quiz',
    ]

    for proc in procedures:
        op.execute(f"DROP FUNCTION public.{proc} CASCADE")

def drop_triggers() -> None:
    triggers = [
        'update_about_us_order_numbers_after_delete_trigger ON public.about_us',
        'update_instruction_order_numbers_after_delete_trigger ON public.instruction',
    ]

    for trigger in triggers:
        op.execute(f"DROP TRIGGER {trigger}")


def upgrade() -> None:
    create_insert_public_procedures()
    create_select_public_procedures()
    create_update_public_procedures()
    create_delete_public_procedures()
    create_quiz_handling_functions()
    create_on_delete_triggers()

def downgrade() -> None:
    drop_triggers()
    drop_public_procedures()