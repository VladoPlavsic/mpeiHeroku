"""front_page_reviews
Revision ID: c27dd31a70ad
Revises: 3ddd879e1720
Create Date: 2021-10-26 15:04:34.193027
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = 'c27dd31a70ad'
down_revision = '3ddd879e1720'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "reviews",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.Text, nullable=False),
        sa.Column("review", sa.Text, nullable=False),
        sa.Column("object_key", sa.Text, nullable=True),
        sa.Column("image_url", sa.Text, nullable=True),
        schema='public'
    )

    op.execute("""
    CREATE OR REPLACE FUNCTION public.insert_review(name_ TEXT, review_ TEXT, object_key_ TEXT, image_url_ TEXT)
    RETURNS TABLE(id INT, name TEXT, review TEXT, object_key TEXT, image_url TEXT)
    AS $$
    DECLARE 
        id_ INT;
    BEGIN
        INSERT INTO public.reviews(name, review, object_key, image_url) VALUES(name_, review_, object_key_, image_url_) RETURNING public.reviews.id INTO id_;
        RETURN QUERY(SELECT * FROM public.reviews WHERE public.reviews.id = id_);
    END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION public.select_all_reviews()
    RETURNS TABLE(id INT, name TEXT, review TEXT, object_key TEXT, image_url TEXT)
    AS $$
    BEGIN
        RETURN QUERY(SELECT * FROM public.reviews);
    END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION public.update_review(id_ INT, name_ TEXT, review_ TEXT, object_key_ TEXT, image_url_ TEXT)
    RETURNS TABLE(id INT, name TEXT, review TEXT, object_key TEXT, image_url TEXT)
    AS $$
    BEGIN
        UPDATE public.reviews SET 
            name = COALESCE(name_, public.reviews.name),
            review = COALESCE(review_, public.reviews.review),
            object_key = COALESCE(object_key_, public.reviews.object_key),
            image_url = COALESCE(image_url_, public.reviews.image_url)
        WHERE public.reviews.id = id_; 
        RETURN QUERY(SELECT * FROM public.reviews WHERE public.reviews.id = id_);
    END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION public.delete_review(id_ INT)
    RETURNS VOID
    AS $$
    BEGIN
        DELETE FROM public.reviews WHERE id = id_;
    END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION public.select_all_review_keys()
    RETURNS TABLE(object_key text)
    AS $$
    BEGIN
        RETURN QUERY(SELECT public.reviews.object_key FROM public.reviews);
    END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION public.update_review_links(keys text[], urls text[])
    RETURNS VOID
    AS $$
    BEGIN
        FOR index IN 1 .. array_upper(keys, 1)
        LOOP
            UPDATE public.reviews SET
                image_url = urls[index]
            WHERE object_key = keys[index];
        END LOOP;
    END $$ LANGUAGE plpgsql;
    """)

def drop_functions() -> None:
    functions = [
        'insert_review',
        'select_all_reviews',
        'update_review',
        'delete_review',
        'select_all_review_keys',
        'update_review_links',
    ]

    for function in functions:
        op.execute(f"DROP FUNCTION public.{function}")

def downgrade() -> None:
    op.execute("DROP TABLE public.reviews")
    drop_functions()

