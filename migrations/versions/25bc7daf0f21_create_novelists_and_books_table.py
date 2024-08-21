"""create novelists and livros table

Revision ID: 25bc7daf0f21
Revises: 7f4cad54840e
Create Date: 2024-08-20 18:20:18.896895

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '25bc7daf0f21'
down_revision: Union[str, None] = '7f4cad54840e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('novelists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('livros',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('titulo', sa.String(), nullable=False),
    sa.Column('ano', sa.Integer(), nullable=False),
    sa.Column('novelist_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['novelist_id'], ['novelists.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('titulo')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('livros')
    op.drop_table('novelists')
    # ### end Alembic commands ###
