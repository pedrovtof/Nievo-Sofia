"""set grant for auth user in accounts

Revision ID: a1ec85b0f442
Revises: 7312727d435c
Create Date: 2026-10-27 09:40:46.110965

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1ec85b0f442'
down_revision = '7312727d435c'
branch_labels = None
depends_on = None


def upgrade():
    """Grant schema, table, and sequence privileges in accounts to platform_auth."""
    op.execute("""
        GRANT CONNECT ON DATABASE accounts TO platform_auth;
        GRANT USAGE ON SCHEMA member TO platform_auth;
        GRANT USAGE ON SCHEMA signup TO platform_auth;
        GRANT SELECT, INSERT, UPDATE ON TABLE member.device TO platform_auth;
        GRANT SELECT, INSERT, UPDATE ON TABLE member.user TO platform_auth;
        GRANT SELECT, INSERT, UPDATE ON TABLE member.user_details TO platform_auth;
        GRANT SELECT, INSERT, UPDATE ON TABLE signup.country TO platform_auth;
        GRANT SELECT, INSERT, UPDATE ON TABLE signup.terms TO platform_auth;
        GRANT SELECT, INSERT, UPDATE ON TABLE signup.user_agreements TO platform_auth;
        ALTER DEFAULT PRIVILEGES IN SCHEMA member GRANT USAGE, SELECT ON SEQUENCES TO platform_auth;
        ALTER DEFAULT PRIVILEGES IN SCHEMA signup GRANT USAGE, SELECT ON SEQUENCES TO platform_auth;
        GRANT ALL ON SEQUENCE signup.country_id_seq TO platform_auth;
        GRANT ALL ON SEQUENCE signup.terms_id_seq TO platform_auth;
    """)
    pass


def downgrade():
    """Revoke schema, table, and sequence privileges in accounts from platform_auth."""
    op.execute("""
        REVOKE CONNECT ON DATABASE accounts FROM platform_auth;
        REVOKE USAGE ON SCHEMA member FROM platform_auth;
        REVOKE USAGE ON SCHEMA signup FROM platform_auth;
        REVOKE SELECT, INSERT, UPDATE ON TABLE member.device FROM platform_auth;
        REVOKE SELECT, INSERT, UPDATE ON TABLE member.user FROM platform_auth;
        REVOKE SELECT, INSERT, UPDATE ON TABLE member.user_details FROM platform_auth;
        REVOKE SELECT, INSERT, UPDATE ON TABLE signup.country FROM platform_auth;
        REVOKE SELECT, INSERT, UPDATE ON TABLE signup.terms FROM platform_auth;
        REVOKE SELECT, INSERT, UPDATE ON TABLE signup.user_agreements FROM platform_auth;
        ALTER DEFAULT PRIVILEGES IN SCHEMA member REVOKE USAGE, SELECT ON SEQUENCES FROM platform_auth;
        ALTER DEFAULT PRIVILEGES IN SCHEMA signup REVOKE USAGE, SELECT ON SEQUENCES FROM platform_auth;
        REVOKE ALL ON SEQUENCE signup.country_id_seq FROM platform_auth;
        REVOKE ALL ON SEQUENCE signup.terms_id_seq FROM platform_auth;
    """)
    pass
