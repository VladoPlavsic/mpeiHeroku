"""About functions
Revision ID: 91c0fe2ebacf
Revises: 823edd886cde
Create Date: 2021-04-06 14:17:16.493829
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '91c0fe2ebacf'
down_revision = '823edd886cde'
branch_labels = None
depends_on = None

def create_insert_functions() -> None:
    # our team
    op.execute('''
    CREATE OR REPLACE FUNCTION about.insert_our_team(i_order int, i_name text, i_role text, i_profession text, i_description text, i_photo_key text, i_photo_link text)
        RETURNS TABLE ("order" int, name text, role text, profession text, description text, photo_key text, photo_link text)
        AS $$
        DECLARE 
            inserted_id int;
        BEGIN 
        INSERT INTO about.our_team ("order", name, role, profession, description, photo_key, photo_link)
        VALUES (i_order, i_name, i_role,i_profession, i_description, i_photo_key, i_photo_link) RETURNING about.our_team."order" INTO inserted_id;
        RETURN QUERY (SELECT * FROM about.our_team WHERE about.our_team.order = inserted_id);
        END $$ LANGUAGE plpgsql;
    ''')
    # contacts
    op.execute('''
    CREATE OR REPLACE FUNCTION about.insert_contacts(i_order int, i_html text)
        RETURNS TABLE ("order" int, html text)
        AS $$
        DECLARE
            inserted_id int;
        BEGIN 
        INSERT INTO about.contacts ("order", html)
        VALUES (i_order, i_html) RETURNING about.contacts.order INTO inserted_id;
        RETURN QUERY (SELECT * FROM about.contacts WHERE about.contacts.order = inserted_id);
        END $$ LANGUAGE plpgsql;
    ''')
    # about project
    op.execute('''
    CREATE OR REPLACE FUNCTION about.insert_about_project(i_order int, i_html text)
        RETURNS TABLE ("order" int, html text)
        AS $$
        DECLARE
            inserted_id int;
        BEGIN 
        INSERT INTO about.about_project ("order", html)
        VALUES (i_order, i_html) RETURNING about.about_project.order INTO inserted_id;
        RETURN QUERY (SELECT * FROM about.about_project WHERE about.about_project.order = inserted_id);
        END $$ LANGUAGE plpgsql;
    ''')
    

def create_update_functions() -> None:
    # update teeam member photo links
    op.execute('''
    CREATE OR REPLACE FUNCTION about.update_team_member_photos(photo_keys text[], photo_links text[])
        RETURNS VOID
        AS $$
        BEGIN
        FOR index IN 1 .. array_upper(photo_keys, 1)
        LOOP
            UPDATE about.our_team SET
            photo_link = photo_links[index] 
            WHERE photo_key = photo_keys[index];
        END LOOP;
        END $$ LANGUAGE plpgsql;
    ''')
    # update team member
    op.execute('''
    CREATE OR REPLACE FUNCTION about.update_team_member(id int, i_order int, i_name text, i_role text, i_profession text, i_photo_key text, i_photo_link text,  i_description text)
        RETURNS TABLE ("order" int, name text, role text, profession text, description text, photo_key text, photo_link text)
        AS $$
        BEGIN
        UPDATE about.our_team SET
            "order" = COALESCE(i_order, about.our_team.order),
            name = COALESCE(i_name, about.our_team.name),
            role = COALESCE(i_role, about.our_team.role),
            profession = COALESCE(i_profession, about.our_team.profession), 
            description = COALESCE(i_description, about.our_team.description),
            photo_key = COALESCE(i_photo_key, about.our_team.photo_key),
            photo_link = COALESCE(i_photo_link, about.our_team.photo_link)
        WHERE about.our_team.order = id;
        RETURN QUERY (SELECT * FROM about.our_team WHERE about.our_team.order = COALESCE(i_order, id));
        END $$ LANGUAGE plpgsql;
    ''')
    # update about project
    op.execute('''
    CREATE OR REPLACE FUNCTION about.update_about_project(id int, i_order int, i_html text)
        RETURNS TABLE ("order" int, html text)
        AS $$
        BEGIN
        UPDATE about.about_project SET
            "order" = COALESCE(i_order, about.about_project.order),
            html = COALESCE(i_html, about.about_project.html)
        WHERE about.about_project.order = id;
        RETURN QUERY (SELECT * FROM about.about_project WHERE about.about_project.order = COALESCE(i_order, id));
        END $$ LANGUAGE plpgsql;
    ''')
    # update contact
    op.execute('''
    CREATE OR REPLACE FUNCTION about.update_contact(id int, i_order int, i_html text)
        RETURNS TABLE ("order" int, html text)
        AS $$
        BEGIN
        UPDATE about.contacts SET
            "order" = COALESCE(i_order, about.contacts.order),
            html = COALESCE(i_html, about.contacts.html)
        WHERE about.contacts.order = id;
        RETURN QUERY (SELECT * FROM about.contacts WHERE about.contacts.order = COALESCE(i_order, id));
        END $$ LANGUAGE plpgsql;
    ''')

def create_select_functions() -> None:
    # select all team members
    op.execute('''
    CREATE OR REPLACE FUNCTION about.select_all_team_members()
        RETURNS TABLE ("order" int, name text, role text, profession text, description text, photo_key text, photo_link text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM about.our_team ORDER BY "order");
        END $$ LANGUAGE plpgsql;
    ''')
    # select all about project
    op.execute('''
    CREATE OR REPLACE FUNCTION about.select_all_about_project()
        RETURNS TABLE ("order" int, html text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM about.about_project ORDER BY "order");
        END $$ LANGUAGE plpgsql;
    ''')
    # select all contacts
    op.execute('''
    CREATE OR REPLACE FUNCTION about.select_all_contacts()
        RETURNS TABLE ("order" int, html text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM about.contacts ORDER BY "order");
        END $$ LANGUAGE plpgsql;
    ''')

def create_delete_functions() -> None:
    # delete team member
    op.execute('''
    CREATE OR REPLACE FUNCTION about.delete_team_member(id int)
        RETURNS VOID 
        AS $$
        BEGIN 
        DELETE FROM about.our_team WHERE "order" = id;
        END $$ LANGUAGE plpgsql;
    ''')
    # delete about project
    op.execute('''
    CREATE OR REPLACE FUNCTION about.delete_about_project(id int)
        RETURNS VOID 
        AS $$
        BEGIN 
        DELETE FROM about.about_project WHERE "order" = id;
        END $$ LANGUAGE plpgsql;
    ''')
    # delete contact
    op.execute('''
    CREATE OR REPLACE FUNCTION about.delete_contact(id int)
        RETURNS VOID
        AS $$
        BEGIN
        DELETE FROM about.contacts WHERE "order" = id;
        END $$ LANGUAGE plpgsql;
    ''')


def drop_functions() -> None:
    functions = [
        'insert_our_team',
        'insert_contacts',
        'insert_about_project',
        'select_all_team_members',
        'update_team_member_photos',
        'select_all_contacts',
        'select_all_about_project',
        'delete_contact',
        'delete_about_project',
        'delete_team_member',
        'update_team_member',
        'update_about_project',
        'update_contact',]

    for function in functions:
        op.execute(f"DROP FUNCTION about.{function}")


def upgrade() -> None:
    create_insert_functions()
    create_select_functions()
    create_update_functions()
    create_delete_functions()

def downgrade() -> None:
    drop_functions()