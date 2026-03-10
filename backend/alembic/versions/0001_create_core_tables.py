"""Create users, images, and results tables

Revision ID: 0001_create_core_tables
Revises:
Create Date: 2026-03-05 00:00:00.000000

"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "0001_create_core_tables"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Users table
    op.create_table(
        "users",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
        ),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.Column("full_name", sa.String(), nullable=True),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=False),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=False),
            nullable=False,
        ),
    )
    op.create_index("ix_users_id", "users", ["id"], unique=False)
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    # Images table
    op.create_table(
        "images",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
        ),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("original_filename", sa.String(), nullable=False),
        sa.Column("storage_path", sa.String(), nullable=False),
        sa.Column("width", sa.Integer(), nullable=False),
        sa.Column("height", sa.Integer(), nullable=False),
        sa.Column(
            "uploaded_at",
            sa.DateTime(timezone=False),
            nullable=False,
        ),
        sa.Column(
            "deleted",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )
    op.create_index("ix_images_id", "images", ["id"], unique=False)
    op.create_index("ix_images_user_id", "images", ["user_id"], unique=False)

    # Results table
    op.create_table(
        "results",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
        ),
        sa.Column(
            "image_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("images.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("model_type", sa.String(), nullable=False),
        sa.Column("scale_factor", sa.Integer(), nullable=False),
        sa.Column("output_path", sa.String(), nullable=False),
        sa.Column("psnr", sa.Float(), nullable=False),
        sa.Column("ssim", sa.Float(), nullable=False),
        sa.Column("mse", sa.Float(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=False),
            nullable=False,
        ),
        sa.Column("processing_time_ms", sa.Integer(), nullable=True),
    )
    op.create_index("ix_results_id", "results", ["id"], unique=False)
    op.create_index("ix_results_image_id", "results", ["image_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_results_image_id", table_name="results")
    op.drop_index("ix_results_id", table_name="results")
    op.drop_table("results")

    op.drop_index("ix_images_user_id", table_name="images")
    op.drop_index("ix_images_id", table_name="images")
    op.drop_table("images")

    op.drop_index("ix_users_email", table_name="users")
    op.drop_index("ix_users_id", table_name="users")
    op.drop_table("users")
