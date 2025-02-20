"""Remove participacion_cuatro

Revision ID: 815be4d9adb1
Revises: f8a7bc741a4d
Create Date: 2025-02-20 19:16:14.241244

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '815be4d9adb1'
down_revision = 'f8a7bc741a4d'
branch_labels = None
depends_on = None


def upgrade():
    # SOLO quitamos la columna participacion_cuatro usando "batch mode" en SQLite
    with op.batch_alter_table('participacion', schema=None) as batch_op:
        batch_op.drop_column('participacion_cuatro')


def downgrade():
    # Si retrocedemos la migración, volvemos a crear la columna
    with op.batch_alter_table('participacion', schema=None) as batch_op:
        batch_op.add_column(sa.Column('participacion_cuatro', sa.VARCHAR(length=120), nullable=False))
