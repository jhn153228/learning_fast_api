"""Initial migration: create users table
Revision ID: 001
Revises: 
Create Date: 2026-02-10
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
revision: str = "001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_index("idx_user_email", "users", ["email"], unique=True)
    op.create_index("idx_user_created_at", "users", ["created_at"], unique=False)
def downgrade() -> None:
    op.drop_index("idx_user_created_at", table_name="users")
    op.drop_index("idx_user_email", table_name="users")
    op.drop_table("users")
