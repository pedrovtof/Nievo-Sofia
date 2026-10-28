"""create tables for schema member

Revision ID: dab5b850a8db
Revises: 22e629197d2b
Create Date: 2026-10-26 21:33:34.907951

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dab5b850a8db'
down_revision = '22e629197d2b'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        CREATE TABLE IF NOT EXISTS member.user (
            id uuid primary key,
            full_name VARCHAR(150) default null,
            nick_name VARCHAR(150) default null,
            email varchar(150) default null,
            phone varchar(50) default null,
            active bool default true not null,
            created_at TIMESTAMP default CURRENT_TIMESTAMP not null,
            updated_at TIMESTAMP default CURRENT_TIMESTAMP not null
        );

        CREATE TABLE IF NOT EXISTS member.user_details (
            id uuid primary key,
            user_id uuid not null,
            born_date date not null,
            country_id int default null,
            validated_email bool default false not null,
            validated_phone bool default false not null,
            address varchar(50) default null,
            document varchar(50) not null,
            created_at TIMESTAMP default CURRENT_TIMESTAMP not null,
            updated_at TIMESTAMP default CURRENT_TIMESTAMP not null
        );

        CREATE TABLE IF NOT EXISTS member.device (
            id uuid primary key,
            user_id uuid not null,
            x_device_id varchar(50) not null,
            ip_list varchar[] default null,
            active bool default true not null,
            created_at TIMESTAMP default CURRENT_TIMESTAMP not null,
            updated_at TIMESTAMP default CURRENT_TIMESTAMP not null
        );   
    """)
    pass


def downgrade():
    op.execute("""
        DROP TABLE IF EXISTS  member.device;
        DROP TABLE IF EXISTS  member.user_details;
        DROP TABLE IF EXISTS  member.user;
    """)
    pass
