"""user email not important

Revision ID: f75c6f542395
Revises: ddd5aecb091b
Create Date: 2025-09-08 23:41:09.148459

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f75c6f542395'
down_revision: Union[str, Sequence[str], None] = 'ddd5aecb091b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    with op.batch_alter_table('users') as batch_op:
        batch_op.create_unique_constraint('uq_users_email', ['email'])

def downgrade():
    with op.batch_alter_table('users') as batch_op:
        batch_op.drop_constraint('uq_users_email', type_='unique')