"""Added username to user

Revision ID: e3c80d85a970
Revises: 6ed46d8d3057
Create Date: 2025-10-14 06:36:45.504369

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e3c80d85a970'
down_revision: Union[str, None] = '6ed46d8d3057'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
