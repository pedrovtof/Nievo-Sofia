"""create index and references in members

Revision ID: bb147f4b4e5c
Revises: 7172f95175c9
Create Date: 2026-10-27 07:32:28.561963

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb147f4b4e5c'
down_revision = '7172f95175c9'
branch_labels = None
depends_on = None

def upgrade():
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_member_user_details') THEN
                ALTER TABLE member.user_details
                ADD CONSTRAINT fk_member_user_details FOREIGN KEY (user_id) REFERENCES member.user(id);
            END IF;

            IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_member_user_device') THEN
                ALTER TABLE member.device
                ADD CONSTRAINT fk_member_user_device FOREIGN KEY (user_id) REFERENCES member.user(id);
            END IF;

            IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_member_user_details_contry') THEN
                ALTER TABLE member.user_details
                ADD CONSTRAINT fk_member_user_details_contry FOREIGN KEY (country_id) REFERENCES signup.country(id);
            END IF;
        END $$;

        CREATE UNIQUE INDEX IF NOT EXISTS un_idx_members_detail_user_id ON  member.user_details (user_id);

        CREATE UNIQUE INDEX IF NOT EXISTS un_idx_members_detail_user_document ON  member.user_details (document);

        CREATE UNIQUE INDEX IF NOT EXISTS un_idx_members_email ON  member.user (email);

        CREATE UNIQUE INDEX IF NOT EXISTS un_idx_members_phone ON  member.user (phone);
    """)
    pass


def downgrade():
    op.execute("""
        DO $$
            BEGIN

            IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_member_user_details') THEN
                ALTER TABLE member.user_details
                DROP CONSTRAINT fk_member_user_details;
            END IF;

            IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_member_user_device') THEN
                ALTER TABLE member.device
                DROP CONSTRAINT fk_member_user_device;
            END IF;

            IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_member_user_details_contry') THEN
                ALTER TABLE member.user_details
                DROP CONSTRAINT fk_member_user_details_contry;
            END IF;
        END $$;

        DROP INDEX IF EXISTS member.un_idx_members_detail_user_id;

        DROP INDEX IF EXISTS member.un_idx_members_detail_user_document;

        DROP INDEX IF EXISTS member.un_idx_members_email;

        DROP INDEX IF EXISTS member.un_idx_members_phone;
    """)
    pass
