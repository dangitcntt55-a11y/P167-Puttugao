"""split ai_engine into llm_engine + search_engine

Revision ID: 0001
Revises:
Create Date: 2026-08-02
"""
from alembic import op
import sqlalchemy as sa


revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1) responses: add columns nullable trước để không break existing rows
    op.add_column("responses", sa.Column("llm_engine", sa.String(20), nullable=True))
    op.add_column("responses", sa.Column("search_engine", sa.String(20), nullable=True))
    op.create_index("idx_responses_llm_engine", "responses", ["llm_engine"])
    op.create_index("idx_responses_search_engine", "responses", ["search_engine"])

    # 2) Migrate data: ai_engine ∈ {chatgpt, gemini, claude} → llm_engine
    op.execute(
        """
        UPDATE responses
        SET llm_engine = ai_engine
        WHERE ai_engine IN ('chatgpt', 'gemini', 'claude')
        """
    )
    op.execute(
        """
        UPDATE responses
        SET search_engine = ai_engine
        WHERE ai_engine = 'tavily'
        """
    )

    # 3) Drop old column + index
    op.drop_index("idx_responses_ai_engine", table_name="responses")
    op.drop_column("responses", "ai_engine")

    # 4) Check constraint: chỉ 1 trong 2 engine columns NOT NULL
    op.create_check_constraint(
        "chk_one_engine",
        "responses",
        "(llm_engine IS NOT NULL AND search_engine IS NULL) "
        "OR (llm_engine IS NULL AND search_engine IS NOT NULL)",
    )

    # 5) stability_scores: cùng pattern (cả 2 NULL = aggregate overall)
    op.add_column("stability_scores", sa.Column("llm_engine", sa.String(20), nullable=True))
    op.add_column("stability_scores", sa.Column("search_engine", sa.String(20), nullable=True))
    op.create_index("idx_stability_llm_engine", "stability_scores", ["llm_engine"])
    op.create_index("idx_stability_search_engine", "stability_scores", ["search_engine"])

    op.execute(
        """
        UPDATE stability_scores
        SET llm_engine = ai_engine
        WHERE ai_engine IN ('chatgpt', 'gemini', 'claude')
        """
    )
    op.execute(
        """
        UPDATE stability_scores
        SET search_engine = ai_engine
        WHERE ai_engine = 'tavily'
        """
    )

    op.drop_index("idx_stability_ai_engine", table_name="stability_scores")
    op.drop_column("stability_scores", "ai_engine")

    op.create_check_constraint(
        "chk_stability_one_engine",
        "stability_scores",
        "(llm_engine IS NOT NULL AND search_engine IS NULL) "
        "OR (llm_engine IS NULL AND search_engine IS NOT NULL) "
        "OR (llm_engine IS NULL AND search_engine IS NULL)",
    )


def downgrade() -> None:
    # 1) Reverse stability_scores
    op.drop_constraint("chk_stability_one_engine", "stability_scores", type_="check")
    op.add_column("stability_scores", sa.Column("ai_engine", sa.String(20), nullable=True))
    op.execute(
        """
        UPDATE stability_scores
        SET ai_engine = COALESCE(llm_engine, search_engine)
        """
    )
    op.create_index("idx_stability_ai_engine", "stability_scores", ["ai_engine"])
    op.drop_column("stability_scores", "search_engine")
    op.drop_index("idx_stability_search_engine", table_name="stability_scores")
    op.drop_column("stability_scores", "llm_engine")
    op.drop_index("idx_stability_llm_engine", table_name="stability_scores")

    # 2) Reverse responses
    op.drop_constraint("chk_one_engine", "responses", type_="check")
    op.add_column("responses", sa.Column("ai_engine", sa.String(20), nullable=True))
    op.execute(
        """
        UPDATE responses
        SET ai_engine = COALESCE(llm_engine, search_engine)
        """
    )
    op.create_index("idx_responses_ai_engine", "responses", ["ai_engine"])
    op.drop_column("responses", "search_engine")
    op.drop_index("idx_responses_search_engine", table_name="responses")
    op.drop_column("responses", "llm_engine")
    op.drop_index("idx_responses_llm_engine", table_name="responses")