"""create schema signup

Revision ID: 1e54206ef92a
Revises: 
Create Date: 2026-10-26 21:31:06.629328

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e54206ef92a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        CREATE SCHEMA IF NOT EXISTS signup;
    """)
    pass


def downgrade():
    op.execute("""
        DROP SCHEMA IF EXISTS signup CASCADE;      
    """)
    pass
