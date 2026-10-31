"""create schema member

Revision ID: 22e629197d2b
Revises: 1e54206ef92a
Create Date: 2026-10-26 21:31:12.156618

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22e629197d2b'
down_revision = '1e54206ef92a'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        CREATE SCHEMA IF NOT EXISTS member; 
    """)
    pass


def downgrade():
    op.execute("""
        DROP SCHEMA IF EXISTS member CASCADE;
    """)
    pass
