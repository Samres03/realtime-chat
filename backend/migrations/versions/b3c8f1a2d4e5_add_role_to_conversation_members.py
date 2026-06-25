"""add role to conversation_members

Revision ID: b3c8f1a2d4e5
Revises: aab05bcd8067
Create Date: 2026-06-11 12:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "b3c8f1a2d4e5"
down_revision: Union[str, Sequence[str], None] = "aab05bcd8067"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "conversation_members",
        sa.Column(
            "role",
            sa.String(length=20),
            server_default="member",
            nullable=False,
        ),
    )
    op.alter_column("conversation_members", "role", server_default=None)


def downgrade() -> None:
    op.drop_column("conversation_members", "role")
