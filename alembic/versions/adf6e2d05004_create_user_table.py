"""create user table

Revision ID: adf6e2d05004
Revises: 2bb64ab13fd2
Create Date: 2022-10-21 23:49:59.843631

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'adf6e2d05004'
down_revision = '2bb64ab13fd2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users",
                    sa.Column("id", sa.Integer,
                              nullable=False),
                    sa.Column("user_name", sa.String, nullable=False),
                    sa.Column("email", sa.String, nullable=False),
                    sa.Column("password", sa.String, nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                              nullable=False, server_default=sa.text("now()"),
                              ),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("email"))
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
