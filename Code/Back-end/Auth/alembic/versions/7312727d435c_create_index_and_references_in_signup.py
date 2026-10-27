"""create index and references in signup

Revision ID: 7312727d435c
Revises: bb147f4b4e5c
Create Date: 2026-10-27 07:32:34.706207

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7312727d435c'
down_revision = 'bb147f4b4e5c'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_user_agreements_term') THEN
                ALTER TABLE signup.user_agreements
                ADD CONSTRAINT fk_user_agreements_term FOREIGN KEY (term_id) REFERENCES signup.terms(id);
            END IF;

            IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_user_agreements_user') THEN
                ALTER TABLE signup.user_agreements
                ADD CONSTRAINT fk_user_agreements_user FOREIGN KEY (user_id) REFERENCES member.user(id);
            END IF;
        END $$;

        CREATE UNIQUE INDEX IF NOT EXISTS un_idx_signup_user_agreements ON  signup.user_agreements (user_id,term_id);

        CREATE UNIQUE INDEX IF NOT EXISTS un_idx_signup_terms ON signup.terms (tag,version);

        CREATE UNIQUE INDEX IF NOT EXISTS un_idx_signup_contry ON signup.contry (tag);
    """)
    pass


def downgrade():
    op.execute("""
        DO $$
            BEGIN

            IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_user_agreements_term') THEN
                ALTER TABLE signup.user_agreements
                DROP CONSTRAINT fk_user_agreements_term;
            END IF;

            IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_user_agreements_user') THEN
                ALTER TABLE signup.user_agreements
                DROP CONSTRAINT fk_user_agreements_user;
            END IF;
        END $$;


        DROP INDEX IF EXISTS signup.un_idx_signup_user_agreements;

        DROP INDEX IF EXISTS signup.un_idx_signup_terms;

        DROP INDEX IF EXISTS signup.un_idx_signup_contry;
    """)
    pass
