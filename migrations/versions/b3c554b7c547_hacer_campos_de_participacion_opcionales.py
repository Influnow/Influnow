"""Hacer campos de participacion opcionales

Revision ID: b3c554b7c547
Revises: 815be4d9adb1
Create Date: 2025-03-22 11:15:39.493910
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3c554b7c547'
down_revision = '815be4d9adb1'
branch_labels = None
depends_on = None


def upgrade():
    # Eliminar columna en agent_request usando batch (SQLite requiere esto)
    with op.batch_alter_table('agent_request', schema=None) as batch_op:
        batch_op.drop_column('user_id')

    # Cambios en contactos (usar batch por SQLite)
    with op.batch_alter_table('contactos', schema=None) as batch_op:
        batch_op.alter_column('contacto_nombre',
            existing_type=sa.VARCHAR(length=150),
            type_=sa.String(length=50),
            nullable=False)
        batch_op.alter_column('contacto_telefono',
            existing_type=sa.VARCHAR(length=15),
            type_=sa.String(length=20),
            nullable=False)
        batch_op.alter_column('contacto_email',
            existing_type=sa.VARCHAR(length=150),
            type_=sa.String(length=100),
            nullable=False)
        batch_op.alter_column('contacto_mensaje',
            existing_type=sa.TEXT(),
            nullable=False)

    # Cambios en participacion (usar batch por SQLite)
    with op.batch_alter_table('participacion', schema=None) as batch_op:
        batch_op.alter_column('user_id',
            existing_type=sa.INTEGER(),
            nullable=False)
        batch_op.alter_column('participacion_uno',
            existing_type=sa.VARCHAR(length=100),
            type_=sa.Text(),
            nullable=True)
        batch_op.alter_column('participacion_dos',
            existing_type=sa.VARCHAR(length=100),
            type_=sa.Text(),
            nullable=True)
        batch_op.alter_column('participacion_tres',
            existing_type=sa.VARCHAR(length=100),
            type_=sa.Text(),
            nullable=True)


def downgrade():
    # Revertir cambios en tabla participacion con batch_alter_table
    with op.batch_alter_table('participacion', schema=None) as batch_op:
        batch_op.alter_column('participacion_tres',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('participacion_dos',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('participacion_uno',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # Revertir cambios en tabla contactos
    op.alter_column('contactos', 'contacto_mensaje',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('contactos', 'contacto_email',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=150),
               nullable=True)
    op.alter_column('contactos', 'contacto_telefono',
               existing_type=sa.String(length=20),
               type_=sa.VARCHAR(length=15),
               nullable=True)
    op.alter_column('contactos', 'contacto_nombre',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=150),
               nullable=True)

    # Restaurar columna y relación en agent_request
    op.add_column('agent_request', sa.Column('user_id', sa.INTEGER(), nullable=False))
    op.create_foreign_key(None, 'agent_request', 'user', ['user_id'], ['id'])
