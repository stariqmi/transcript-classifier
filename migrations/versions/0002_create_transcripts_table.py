"""create transcripts table

Revision ID: 0002_create_transcripts_table
Revises: 
Create Date: 2024-xx-xx

"""
from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector

# revision identifiers, used by Alembic.
revision = '0002_create_transcripts_table'
down_revision = '0001_create_catalogue_table'
branch_labels = None
depends_on = None

def upgrade():
    # Create vector extension if it doesn't exist
    op.execute('CREATE EXTENSION IF NOT EXISTS vector')

    # Create transcripts table
    op.create_table(
        'transcripts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('file_name', sa.String(), nullable=False),
        sa.Column('transcript_data', sa.Text(), nullable=True),
        sa.Column('classification', sa.String(), nullable=True),
        sa.Column('embedding', Vector(384), nullable=True), # sentence-transformers/all-MiniLM-L6-v2
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('transcripts') 