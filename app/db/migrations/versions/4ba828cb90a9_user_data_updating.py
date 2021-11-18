"""user_data_updating
Revision ID: 4ba828cb90a9
Revises: 5530af02dfea
Create Date: 2021-11-17 15:58:08.846515
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '4ba828cb90a9'
down_revision = '5530af02dfea'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute("""
    CREATE OR REPLACE FUNCTION users.update_personal_information(id_ INT, full_name_ TEXT, phone_number_ VARCHAR(20), city_ TEXT, school_ TEXT)
    RETURNS TABLE (id INT, full_name text, email text, phone_number varchar(20), city text, school text)
    AS $$
    BEGIN
        UPDATE users.users SET
            full_name = COALESCE(full_name_, users.users.full_name),
            phone_number = COALESCE(phone_number_, users.users.phone_number),
            city = COALESCE(city_, users.users.city),
            school = COALESCE(school_, users.users.school)
        WHERE users.users.id = id_;
        RETURN QUERY(SELECT users.users.id, users.users.full_name, users.users.email, users.users.phone_number, users.users.city, users.users.school FROM users.users WHERE users.users.id = id_);
    END $$ LANGUAGE plpgsql;
    """)

def downgrade() -> None:
    op.execute("DROP FUNCTION users.update_personal_information(INT, TEXT, VARCHAR(20), TEXT, TEXT)")
