"""add onboarding-provisioned ERP username
Revision ID: 6e8a1f2b9c30
Revises: 5d9f2a1c4e77
"""
from alembic import op
import sqlalchemy as sa
revision = "6e8a1f2b9c30"
down_revision = "5d9f2a1c4e77"
branch_labels = None
depends_on = None
def upgrade():
    op.add_column("users", sa.Column("username", sa.String(length=120), nullable=True))
    op.create_index("ix_users_username", "users", ["username"], unique=True)
def downgrade():
    op.drop_index("ix_users_username", table_name="users")
    op.drop_column("users", "username")
