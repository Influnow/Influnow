"""Agregando nuevos campos al modelo User

Revision ID: 3a22ec88fe09
Revises: 
Create Date: 2024-10-06 18:28:08.583204

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a22ec88fe09'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=150), nullable=False),
    sa.Column('apellidos', sa.String(length=150), nullable=False),
    sa.Column('email', sa.String(length=150), nullable=False),
    sa.Column('password', sa.String(length=150), nullable=False),
    sa.Column('movil', sa.String(length=15), nullable=True),
    sa.Column('referido_por', sa.String(length=150), nullable=True),
    sa.Column('saldo', sa.Float(), nullable=True),
    sa.Column('historial_tareas', sa.String(length=500), nullable=True),
    sa.Column('es_administrador', sa.Boolean(), nullable=True),
    sa.Column('cumpleanos', sa.Date(), nullable=True),
    sa.Column('edad', sa.Integer(), nullable=True),
    sa.Column('signo_zodiaco', sa.String(length=50), nullable=True),
    sa.Column('motivo_crear_contenido', sa.String(length=255), nullable=True),
    sa.Column('tipo_contenido', sa.String(length=255), nullable=True),
    sa.Column('tiempo_grabar', sa.String(length=255), nullable=True),
    sa.Column('motivacion', sa.String(length=255), nullable=True),
    sa.Column('conexion_audiencia', sa.String(length=255), nullable=True),
    sa.Column('valor_influencers', sa.String(length=255), nullable=True),
    sa.Column('youtube', sa.String(length=255), nullable=True),
    sa.Column('instagram', sa.String(length=255), nullable=True),
    sa.Column('tiktok', sa.String(length=255), nullable=True),
    sa.Column('twitch', sa.String(length=255), nullable=True),
    sa.Column('mensaje', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.drop_table('agent_request')
    op.drop_table('event')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('event',
        sa.Column('id', sa.INTEGER(), nullable=False),
        sa.Column('user_id', sa.INTEGER(), nullable=False),
        sa.Column('event_name', sa.VARCHAR(length=150), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('agent_request',
        sa.Column('id', sa.INTEGER(), nullable=False),
        sa.Column('user_id', sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('users')
    # ### end Alembic commands ###

    
