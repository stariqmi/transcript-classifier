"""create catalogue table

Revision ID: 0001_create_catalogue_table
Revises: 
Create Date: 2024-xx-xx

"""
from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector

# revision identifiers, used by Alembic.
revision = '0001_create_catalogue_table'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create vector extension if it doesn't exist
    op.execute('CREATE EXTENSION IF NOT EXISTS vector')

    # Create catalogue table
    op.create_table(
        'catalogue',
        sa.Column('course_code', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('embedding', Vector(384), nullable=True), # sentence-transformers/all-MiniLM-L6-v2
        sa.PrimaryKeyConstraint('course_code')
    )

def downgrade():
    op.drop_table('catalogue') 