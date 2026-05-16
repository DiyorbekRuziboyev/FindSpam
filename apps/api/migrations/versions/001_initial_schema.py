"""Initial schema — all bounded contexts

Revision ID: 001
Revises:
Create Date: 2026-05-17
"""

from alembic import op
import sqlalchemy as sa

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ─── users ──────────────────────────────────────────────────────────────
    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("username", sa.String(64), nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("role", sa.String(32), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("is_verified", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_username", "users", ["username"], unique=True)

    # ─── refresh_tokens ──────────────────────────────────────────────────────
    op.create_table(
        "refresh_tokens",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column("token_hash", sa.String(64), nullable=False),
        sa.Column("family_id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revoked_reason", sa.String(64), nullable=True),
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.Column("user_agent", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_refresh_tokens_token_hash", "refresh_tokens", ["token_hash"], unique=True)
    op.create_index("ix_refresh_tokens_family_id", "refresh_tokens", ["family_id"])

    # ─── security_events ─────────────────────────────────────────────────────
    op.create_table(
        "security_events",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column("user_id", sa.UUID(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("event_type", sa.String(32), nullable=False),
        sa.Column("severity", sa.String(16), nullable=False),
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.Column("user_agent", sa.Text(), nullable=True),
        sa.Column("metadata", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_security_events_user_id", "security_events", ["user_id"])
    op.create_index("ix_security_events_event_type", "security_events", ["event_type"])

    # ─── ai_model_versions ───────────────────────────────────────────────────
    op.create_table(
        "ai_model_versions",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("version", sa.String(32), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("metrics", sa.Text(), nullable=True),
        sa.Column("deployed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_ai_model_versions_version", "ai_model_versions", ["version"], unique=True)

    # ─── ai_predictions ──────────────────────────────────────────────────────
    op.create_table(
        "ai_predictions",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column("message_text", sa.Text(), nullable=False),
        sa.Column("language", sa.String(16), nullable=False),
        sa.Column("threat_level", sa.String(16), nullable=False),
        sa.Column("spam_category", sa.String(32), nullable=True),
        sa.Column("confidence_score", sa.Float(), nullable=False),
        sa.Column(
            "model_version_id",
            sa.UUID(),
            sa.ForeignKey("ai_model_versions.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("contributions", sa.Text(), nullable=True),
        sa.Column("explanation", sa.Text(), nullable=True),
        sa.Column("processing_time_ms", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_ai_predictions_threat_level", "ai_predictions", ["threat_level"])

    # ─── ai_feedback ─────────────────────────────────────────────────────────
    op.create_table(
        "ai_feedback",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column(
            "prediction_id",
            sa.UUID(),
            sa.ForeignKey("ai_predictions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("reviewer_id", sa.UUID(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("is_correct", sa.Boolean(), nullable=False),
        sa.Column("correct_label", sa.String(32), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_ai_feedback_prediction_id", "ai_feedback", ["prediction_id"])

    # ─── telegram_groups ─────────────────────────────────────────────────────
    op.create_table(
        "telegram_groups",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column("telegram_id", sa.BigInteger(), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("username", sa.String(128), nullable=True),
        sa.Column("member_count", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("bot_is_admin", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("settings", sa.Text(), nullable=True),
        sa.Column("added_by", sa.UUID(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_telegram_groups_telegram_id", "telegram_groups", ["telegram_id"], unique=True)
    op.create_index("ix_telegram_groups_username", "telegram_groups", ["username"], unique=True)

    # ─── telegram_users ──────────────────────────────────────────────────────
    op.create_table(
        "telegram_users",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column("telegram_id", sa.BigInteger(), nullable=False),
        sa.Column("username", sa.String(128), nullable=True),
        sa.Column("first_name", sa.String(128), nullable=True),
        sa.Column("last_name", sa.String(128), nullable=True),
        sa.Column("is_bot", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("spam_score", sa.Float(), nullable=False, server_default=sa.text("0.0")),
        sa.Column("warning_count", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("is_banned", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("ban_type", sa.String(16), nullable=True),
        sa.Column("banned_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column("ban_reason", sa.Text(), nullable=True),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_telegram_users_telegram_id", "telegram_users", ["telegram_id"], unique=True)
    op.create_index("ix_telegram_users_username", "telegram_users", ["username"])
    op.create_index("ix_telegram_users_is_banned", "telegram_users", ["is_banned"])

    # ─── moderation_events ───────────────────────────────────────────────────
    op.create_table(
        "moderation_events",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column(
            "telegram_group_id",
            sa.UUID(),
            sa.ForeignKey("telegram_groups.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "telegram_user_id",
            sa.UUID(),
            sa.ForeignKey("telegram_users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("message_id", sa.BigInteger(), nullable=False),
        sa.Column("message_text", sa.Text(), nullable=True),
        sa.Column("content_type", sa.String(16), nullable=False),
        sa.Column("threat_level", sa.String(16), nullable=False),
        sa.Column("spam_category", sa.String(32), nullable=True),
        sa.Column("confidence_score", sa.Float(), nullable=True),
        sa.Column(
            "ai_prediction_id",
            sa.UUID(),
            sa.ForeignKey("ai_predictions.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("action_taken", sa.String(32), nullable=False),
        sa.Column("review_status", sa.String(16), nullable=False),
        sa.Column("reviewed_by", sa.UUID(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_moderation_events_telegram_group_id", "moderation_events", ["telegram_group_id"])
    op.create_index("ix_moderation_events_telegram_user_id", "moderation_events", ["telegram_user_id"])
    op.create_index("ix_moderation_events_threat_level", "moderation_events", ["threat_level"])
    op.create_index("ix_moderation_events_action_taken", "moderation_events", ["action_taken"])
    op.create_index("ix_moderation_events_review_status", "moderation_events", ["review_status"])

    # ─── analytics_snapshots ─────────────────────────────────────────────────
    op.create_table(
        "analytics_snapshots",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column("snapshot_date", sa.Date(), nullable=False),
        sa.Column("total_messages", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("spam_detected", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("scam_detected", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("phishing_detected", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("clean_messages", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("avg_confidence", sa.Float(), nullable=False, server_default=sa.text("0.0")),
        sa.Column("total_bans", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("total_warnings", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("total_deletions", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("by_language", sa.Text(), nullable=True),
        sa.Column("by_category", sa.Text(), nullable=True),
        sa.Column("by_threat_level", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_analytics_snapshots_snapshot_date", "analytics_snapshots", ["snapshot_date"], unique=True)

    # ─── blacklist_entries ───────────────────────────────────────────────────
    op.create_table(
        "blacklist_entries",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column("threat_type", sa.String(16), nullable=False),
        sa.Column("value", sa.String(512), nullable=False),
        sa.Column("is_whitelist", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("added_by", sa.UUID(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("hit_count", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_blacklist_entries_threat_type", "blacklist_entries", ["threat_type"])
    op.create_index("ix_blacklist_entries_value", "blacklist_entries", ["value"])
    op.create_index("ix_blacklist_entries_is_whitelist", "blacklist_entries", ["is_whitelist"])
    op.create_unique_constraint(
        "uq_blacklist_type_value", "blacklist_entries", ["threat_type", "value"]
    )

    # ─── audit_logs ──────────────────────────────────────────────────────────
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column("actor_type", sa.String(16), nullable=False),
        sa.Column("actor_id", sa.String(64), nullable=True),
        sa.Column("action", sa.String(128), nullable=False),
        sa.Column("resource_type", sa.String(64), nullable=False),
        sa.Column("resource_id", sa.String(64), nullable=True),
        sa.Column("old_value", sa.Text(), nullable=True),
        sa.Column("new_value", sa.Text(), nullable=True),
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.Column("metadata", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_audit_logs_actor_type", "audit_logs", ["actor_type"])
    op.create_index("ix_audit_logs_actor_id", "audit_logs", ["actor_id"])
    op.create_index("ix_audit_logs_action", "audit_logs", ["action"])
    op.create_index("ix_audit_logs_resource_type", "audit_logs", ["resource_type"])
    op.create_index("ix_audit_logs_created_at", "audit_logs", ["created_at"])


def downgrade() -> None:
    op.drop_table("audit_logs")
    op.drop_table("blacklist_entries")
    op.drop_table("analytics_snapshots")
    op.drop_table("moderation_events")
    op.drop_table("telegram_users")
    op.drop_table("telegram_groups")
    op.drop_table("ai_feedback")
    op.drop_table("ai_predictions")
    op.drop_table("ai_model_versions")
    op.drop_table("security_events")
    op.drop_table("refresh_tokens")
    op.drop_table("users")
