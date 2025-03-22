
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship
db = SQLAlchemy()


# Definimos el modelo de usuario
class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    apellidos = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    movil = db.Column(db.String(15), nullable=True)
    referido_por = db.Column(db.String(150), nullable=True)
    saldo = db.Column(db.Float, default=0.0)
    historial_tareas = db.Column(db.String(500), nullable=True)
    es_administrador = db.Column(db.Boolean, default=False)

    # Campos adicionales para completar el perfil
    cumpleanos = db.Column(db.Date, nullable=True)
    edad = db.Column(db.Integer, nullable=True)
    signo_zodiaco = db.Column(db.String(50), nullable=True)
    motivo_crear_contenido = db.Column(db.String(255), nullable=True)
    tipo_contenido = db.Column(db.String(255), nullable=True)
    tiempo_grabar = db.Column(db.String(255), nullable=True)
    motivacion = db.Column(db.String(255), nullable=True)
    conexion_audiencia = db.Column(db.String(255), nullable=True)
    valor_influencers = db.Column(db.String(255), nullable=True)
    mensaje = db.Column(db.Text, nullable=True)

    # Redes sociales
    youtube = db.Column(db.String(255), nullable=True)
    instagram = db.Column(db.String(255), nullable=True)
    tiktok = db.Column(db.String(255), nullable=True)
    twitch = db.Column(db.String(255), nullable=True)


class Participacion(db.Model):
    __tablename__ = 'participacion'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    participacion_uno = db.Column(db.Text, nullable=True)  # Texto libre para Corte de Borja
    participacion_dos = db.Column(db.Text, nullable=True)  # Texto libre para Vuela Libre
    participacion_tres = db.Column(db.Text, nullable=True)  # Texto libre para Productores Loite

    user = relationship('User', backref='participaciones')


class Contactos(db.Model):
    __tablename__ = 'contactos'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    contacto_nombre = db.Column(db.String(50), nullable=False)
    contacto_telefono = db.Column(db.String(20), nullable=False)
    contacto_email = db.Column(db.String(100), nullable=False)
    contacto_mensaje = db.Column(db.Text, nullable=False)

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_name = db.Column(db.String(150), nullable=False)

class AgentRequest(db.Model):
    __tablename__ = 'agent_request'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)


