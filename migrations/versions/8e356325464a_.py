"""empty message

Revision ID: 8e356325464a
Revises: cb00d1b6ceee
Create Date: 2019-05-17 12:12:58.763248

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8e356325464a'
down_revision = 'cb00d1b6ceee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('telephone', sa.String(length=11), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('answer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('question_id', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('new_user')
    op.drop_table('new_question')
    op.drop_table('new_answer')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('new_answer',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('content', mysql.TEXT(), nullable=False),
    sa.Column('question_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('author_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('create_time', mysql.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['new_user.id'], name='new_answer_ibfk_1'),
    sa.ForeignKeyConstraint(['question_id'], ['new_question.id'], name='new_answer_ibfk_2'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_table('new_question',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('title', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('content', mysql.TEXT(), nullable=False),
    sa.Column('create_time', mysql.DATETIME(), nullable=True),
    sa.Column('author_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['new_user.id'], name='new_question_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_table('new_user',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('telephone', mysql.VARCHAR(length=11), nullable=False),
    sa.Column('username', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('password', mysql.VARCHAR(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.drop_table('answer')
    op.drop_table('question')
    op.drop_table('user')
    # ### end Alembic commands ###
