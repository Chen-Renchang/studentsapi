"""create students table

Revision ID: 8cf0a56fe2c0
Revises: 1c05380c27df
Create Date: 2025-01-16 16:07:58.073517

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8cf0a56fe2c0'
down_revision: Union[str, None] = '1c05380c27df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
