"""add commercial license activations

Revision ID: 1f4b7e8d9a20
Revises: c78895c1dcb8
"""
from alembic import op
import sqlalchemy as sa

revision = "1f4b7e8d9a20"
down_revision = "c78895c1dcb8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "license_activations",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("license_id", sa.String(length=128), nullable=False),
        sa.Column("tenant_id", sa.String(length=128), nullable=False),
        sa.Column("device_id", sa.String(length=255), nullable=False),
        sa.Column("device_name", sa.String(length=255), nullable=True),
        sa.Column("plan", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("max_devices", sa.Integer(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("modules_json", sa.Text(), nullable=False),
        sa.Column("license_payload_json", sa.Text(), nullable=False),
        sa.Column("last_validated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_heartbeat_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("issuer_status", sa.String(length=32), nullable=True),
        sa.Column("revoked", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("license_id", "device_id", name="uq_license_activation_device"),
    )
    op.create_index("ix_license_activations_license_id", "license_activations", ["license_id"])
    op.create_index("ix_license_activations_tenant_id", "license_activations", ["tenant_id"])
    op.create_index("ix_license_activations_device_id", "license_activations", ["device_id"])
    op.create_index("ix_license_activations_status", "license_activations", ["status"])
    op.create_index("ix_license_activations_expires_at", "license_activations", ["expires_at"])


def downgrade() -> None:
    op.drop_table("license_activations")
