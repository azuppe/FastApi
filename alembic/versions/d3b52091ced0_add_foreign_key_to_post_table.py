"""Add foreign key to post table

Revision ID: d3b52091ced0
Revises: adf6e2d05004
Create Date: 2022-10-22 00:09:20.010824

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3b52091ced0'
down_revision = 'adf6e2d05004'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer, nullable = False))
    op.create_foreign_key("post_users_fk", source_table="posts", referent_table="users", local_cols=['owner_id'], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
