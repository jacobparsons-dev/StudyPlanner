"""expand confidence range to 5

Revision ID: 014e11911e6f
Revises: cbd26f9a0d80
Create Date: 2026-03-31 22:54:12.592296

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '014e11911e6f'
down_revision: Union[str, Sequence[str], None] = 'cbd26f9a0d80'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("ck_reviews_confidence", "reviews", type_="check")
    op.create_check_constraint(
        "ck_reviews_confidence",
        "reviews",
        "confidence >= 1 AND confidence <= 5",
    )


def downgrade() -> None:
    op.drop_constraint("ck_reviews_confidence", "reviews", type_="check")
    op.create_check_constraint(
        "ck_reviews_confidence",
        "reviews",
        "confidence >= 1 AND confidence <= 3",
    )