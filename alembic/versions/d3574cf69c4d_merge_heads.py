"""merge_heads

Revision ID: d3574cf69c4d
Revises: 005f803e4a27, e01d17503124
Create Date: 2025-09-16 00:50:18.905296

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd3574cf69c4d'
down_revision: Union[str, Sequence[str], None] = ('005f803e4a27', 'e01d17503124')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
