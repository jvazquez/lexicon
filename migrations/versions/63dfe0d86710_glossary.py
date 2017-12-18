"""glossary

Revision ID: 63dfe0d86710
Revises: 
Create Date: 2017-12-14 18:38:59.359386

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63dfe0d86710'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('terms',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('word', sa.Unicode(length=100), index=True, unique=True),
        sa.Column('definition', sa.UnicodeText(), nullable=False),
        sa.Column('created', sa.DateTime, nullable=True,
                  server_default=sa.func.now()),
        sa.Column('updated', sa.DateTime, nullable=True, onupdate=sa.func.now())
    )

    op.create_table('related_terms',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('term_id', sa.Integer, index=True),
                    sa.Column('related_term_id', sa.Integer, index=True),
                    sa.Column('created', sa.DateTime, nullable=True,
                              server_default=sa.func.now()),
                    sa.Column('updated', sa.DateTime, nullable=True,
                              onupdate=sa.func.now())
    )

    op.create_foreign_key('fk_term_term_id', 'related_terms', 'terms',
                          ['term_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('fk_term_related_term_id', 'related_terms', 'terms',
                          ['related_term_id'], ['id'], ondelete='CASCADE')


def downgrade():
    op.drop_table('related_terms')
    op.drop_table('terms')

