"""create tables for schema signup

Revision ID: 7172f95175c9
Revises: dab5b850a8db
Create Date: 2026-10-26 21:33:40.387650

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7172f95175c9'
down_revision = 'dab5b850a8db'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        CREATE TABLE IF NOT EXISTS signup.terms (
            id serial primary key,
            name varchar(150) not null,
            tag varchar(50) not null,
            content text not null,
            version int default 1 not null,
            active bool default false not null,
            created_at TIMESTAMP default CURRENT_TIMESTAMP not null,
            updated_at TIMESTAMP default CURRENT_TIMESTAMP not null
        );

        CREATE TABLE IF NOT EXISTS signup.user_agreements (
            id uuid primary key,
            user_id uuid not null,
            term_id int not null,
            created_at TIMESTAMP default CURRENT_TIMESTAMP not null
        );

        CREATE TABLE IF NOT EXISTS signup.country (
            id serial primary key,
            tag varchar(10) not null,
            name varchar(150) default null,
            active bool default true not null,
            created_at TIMESTAMP default CURRENT_TIMESTAMP not null,
            updated_at TIMESTAMP default CURRENT_TIMESTAMP not null
        );
    """)
    pass


def downgrade():
    op.execute("""
        DROP TABLE IF EXISTS signup.terms;
        DROP TABLE IF EXISTS signup.country;
        DROP TABLE IF EXISTS signup.user_agreements;
    """)
    pass
