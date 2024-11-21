"""Change password column

Revision ID: 216de1daa72a
Revises: dee0a1cc0f5c
Create Date: 2024-10-30 23:45:02.149961

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "216de1daa72a"
down_revision: Union[str, None] = "dee0a1cc0f5c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user", "hashed_password")
    op.add_column("user", sa.Column("hashed_password", sa.String()))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###