"""Initial depwatch schema.

Revision ID: 20261123_001
Revises:
Create Date: 2026-11-23
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20261123_001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "scans",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("public_token", sa.String(length=64), nullable=False),
        sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("source_type", sa.String(length=16), nullable=False),
        sa.Column("source_summary", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column("total_count", sa.Integer(), nullable=False),
        sa.Column("vulnerable_count", sa.Integer(), nullable=False),
        sa.Column("clean_count", sa.Integer(), nullable=False),
        sa.Column("not_checked_count", sa.Integer(), nullable=False),
        sa.Column("highest_severity", sa.String(length=16), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("public_token"),
    )
    op.create_table(
        "dependency_outcomes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("scan_id", sa.String(length=36), nullable=False),
        sa.Column("line_number", sa.Integer(), nullable=False),
        sa.Column("raw_line", sa.Text(), nullable=False),
        sa.Column("package_name", sa.String(length=255), nullable=True),
        sa.Column("pinned_version", sa.String(length=255), nullable=True),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["scan_id"], ["scans.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "vulnerabilities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("dependency_outcome_id", sa.Integer(), nullable=False),
        sa.Column("osv_id", sa.String(length=255), nullable=False),
        sa.Column("cve_ids", sa.JSON(), nullable=False),
        sa.Column("ghsa_ids", sa.JSON(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("severity_label", sa.String(length=16), nullable=False),
        sa.Column("cvss_score", sa.Float(), nullable=True),
        sa.Column("cvss_vector", sa.Text(), nullable=True),
        sa.Column("severity_source", sa.String(length=16), nullable=False),
        sa.Column("earliest_fixed_version", sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(["dependency_outcome_id"], ["dependency_outcomes.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "browser_history_entries",
        sa.Column("browser_token_hash", sa.String(length=64), nullable=False),
        sa.Column("scan_id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["scan_id"], ["scans.id"]),
        sa.PrimaryKeyConstraint("browser_token_hash", "scan_id"),
    )


def downgrade() -> None:
    op.drop_table("browser_history_entries")
    op.drop_table("vulnerabilities")
    op.drop_table("dependency_outcomes")
    op.drop_table("scans")
