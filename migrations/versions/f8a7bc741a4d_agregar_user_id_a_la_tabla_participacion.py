"""Agregar user_id a la tabla participacion

Revision ID: f8a7bc741a4d
Revises: 6232bff4d4d3
Create Date: 2024-11-10 20:14:24.358965

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'f8a7bc741a4d'
down_revision = '6232bff4d4d3'
branch_labels = None
depends_on = None

def upgrade():
    # Agrega la columna user_id en la tabla participacion y crea la clave foránea
    with op.batch_alter_table('participacion', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))  # nullable=True temporalmente para evitar problemas al agregar
        batch_op.create_foreign_key('fk_user_id', 'user', ['user_id'], ['id'])

def downgrade():
    # Quita la columna user_id y elimina la clave foránea
    with op.batch_alter_table('participacion', schema=None) as batch_op:
        batch_op.drop_constraint('fk_user_id', type_='foreignkey')
        batch_op.drop_column('user_id')
