"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-05-11
"""

from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)

    op.create_table(
        "resumes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("filename", sa.String(length=255), nullable=False),
        sa.Column("extracted_text", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index(op.f("ix_resumes_id"), "resumes", ["id"], unique=False)
    op.create_index(op.f("ix_resumes_user_id"), "resumes", ["user_id"], unique=False)

    op.create_table(
        "job_descriptions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index(op.f("ix_job_descriptions_id"), "job_descriptions", ["id"], unique=False)
    op.create_index(op.f("ix_job_descriptions_user_id"), "job_descriptions", ["user_id"], unique=False)

    op.create_table(
        "match_results",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("resume_id", sa.Integer(), sa.ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("job_description_id", sa.Integer(), sa.ForeignKey("job_descriptions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("match_score", sa.Float(), nullable=False),
        sa.Column("matched_keywords", sa.JSON(), nullable=False),
        sa.Column("missing_keywords", sa.JSON(), nullable=False),
        sa.Column("feedback", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index(op.f("ix_match_results_id"), "match_results", ["id"], unique=False)
    op.create_index(op.f("ix_match_results_user_id"), "match_results", ["user_id"], unique=False)
    op.create_index(op.f("ix_match_results_resume_id"), "match_results", ["resume_id"], unique=False)
    op.create_index(op.f("ix_match_results_job_description_id"), "match_results", ["job_description_id"], unique=False)


def downgrade():
    op.drop_table("match_results")
    op.drop_table("job_descriptions")
    op.drop_table("resumes")
    op.drop_table("users")
