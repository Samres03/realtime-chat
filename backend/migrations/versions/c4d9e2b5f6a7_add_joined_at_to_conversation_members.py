"""add joined_at to conversation_members

Revision ID: c4d9e2b5f6a7
Revises: b3c8f1a2d4e5
Create Date: 2026-06-11 12:30:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "c4d9e2b5f6a7"
down_revision: Union[str, Sequence[str], None] = "b3c8f1a2d4e5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "conversation_members",
        sa.Column(
            "joined_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("conversation_members", "joined_at")
