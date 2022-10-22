"""Add remaining colums to posts tabel

Revision ID: 551dbde6b22b
Revises: d3b52091ced0
Create Date: 2022-10-22 00:19:27.814091

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '551dbde6b22b'
down_revision = 'd3b52091ced0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("published", sa.Boolean, nullable=False, server_default='True'))
    op.add_column("posts",  sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"))),

    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
