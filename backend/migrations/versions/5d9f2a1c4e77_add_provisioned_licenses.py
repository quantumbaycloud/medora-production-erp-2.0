"""merge existing heads and add provisioned licenses

Revision ID: 5d9f2a1c4e77
Revises: 1f4b7e8d9a20, 3ca32b786ec8
"""

from alembic import op
import sqlalchemy as sa


revision = "5d9f2a1c4e77"
down_revision = ("1f4b7e8d9a20", "3ca32b786ec8")
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "provisioned_licenses",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("tenant_id", sa.String(length=128), nullable=False),
        sa.Column("license_id", sa.String(length=128), nullable=False),
        sa.Column("plan", sa.String(length=64), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("license_json", sa.Text(), nullable=False),
        sa.Column("signature", sa.Text(), nullable=False),
        sa.Column(
            "status",
            sa.String(length=32),
            nullable=False,
            server_default="active",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "license_id",
            name="uq_provisioned_licenses_license_id",
        ),
        sa.UniqueConstraint(
            "tenant_id",
            name="uq_provisioned_license_tenant",
        ),
    )

    op.create_index(
        "ix_provisioned_licenses_tenant_id",
        "provisioned_licenses",
        ["tenant_id"],
        unique=False,
    )

    op.create_index(
        "ix_provisioned_licenses_license_id",
        "provisioned_licenses",
        ["license_id"],
        unique=False,
    )

    op.create_index(
        "ix_provisioned_licenses_expires_at",
        "provisioned_licenses",
        ["expires_at"],
        unique=False,
    )

    op.create_index(
        "ix_provisioned_licenses_status",
        "provisioned_licenses",
        ["status"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_provisioned_licenses_status",
        table_name="provisioned_licenses",
    )
    op.drop_index(
        "ix_provisioned_licenses_expires_at",
        table_name="provisioned_licenses",
    )
    op.drop_index(
        "ix_provisioned_licenses_license_id",
        table_name="provisioned_licenses",
    )
    op.drop_index(
        "ix_provisioned_licenses_tenant_id",
        table_name="provisioned_licenses",
    )
    op.drop_table("provisioned_licenses")
