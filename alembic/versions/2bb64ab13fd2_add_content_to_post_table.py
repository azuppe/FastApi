"""add content to post table

Revision ID: 2bb64ab13fd2
Revises: 9b1be2c55a28
Create Date: 2022-10-21 16:54:34.253494

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2bb64ab13fd2'
down_revision = '9b1be2c55a28'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String, nullable = False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")

    pass
