# alembic version
"""Generate table

Revision ID: 3e0c1bf7289a
Revises: 
Create Date: 2023-12-30 09:48:48.891599

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3e0c1bf7289a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user')),
    sa.UniqueConstraint('email', name=op.f('uq_user_email')),
    sa.UniqueConstraint('username', name=op.f('uq_user_username')),
    schema='sirius'
    )
    op.create_index(op.f('ix_sirius_user_id'), 'user', ['id'], unique=False, schema='sirius')
    op.create_table('post',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('content', sa.String(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['sirius.user.id'], name=op.f('fk_post_author_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_post')),
    schema='sirius'
    )
    op.create_index(op.f('ix_sirius_post_id'), 'post', ['id'], unique=False, schema='sirius')
    op.create_table('comment',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('content', sa.String(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['sirius.user.id'], name=op.f('fk_comment_author_id_user')),
    sa.ForeignKeyConstraint(['post_id'], ['sirius.post.id'], name=op.f('fk_comment_post_id_post')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_comment')),
    schema='sirius'
    )
    op.create_index(op.f('ix_sirius_comment_id'), 'comment', ['id'], unique=False, schema='sirius')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_sirius_comment_id'), table_name='comment', schema='sirius')
    op.drop_table('comment', schema='sirius')
    op.drop_index(op.f('ix_sirius_post_id'), table_name='post', schema='sirius')
    op.drop_table('post', schema='sirius')
    op.drop_index(op.f('ix_sirius_user_id'), table_name='user', schema='sirius')
    op.drop_table('user', schema='sirius')
    # ### end Alembic commands ###
