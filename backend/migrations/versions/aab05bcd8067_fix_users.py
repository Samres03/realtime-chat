"""add name to users

Revision ID: aab05bcd8067
Revises: 3685dac9a677
Create Date: 2026-06-02 17:34:46.456483

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "aab05bcd8067"
down_revision: Union[str, Sequence[str], None] = "3685dac9a677"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users", sa.Column("name", sa.String(), nullable=False, server_default="")
    )
    op.alter_column("users", "name", server_default=None)
    op.create_index(op.f("ix_users_name"), "users", ["name"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_users_name"), table_name="users")
    op.drop_column("users", "name")
