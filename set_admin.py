
from app import db, User  # Importar la base de datos y el modelo de usuario desde tu aplicación

# Buscar al usuario por correo electrónico
usuario = User.query.filter_by(email="4740vilo@gmail.com").first()

# Actualizar para que sea administrador
if usuario:
    usuario.es_administrador = True
    db.session.commit()
    print("Usuario actualizado a administrador")
else:
    print("Usuario no encontrado")

