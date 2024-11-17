
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from models import db, User, Participacion, Contactos, Event, AgentRequest 
from datetime import datetime


app = Flask(__name__)

# Obtener el directorio base del proyecto
basedir = os.path.abspath(os.path.dirname(__file__))

# Configuración de SQLAlchemy y otras configuraciones
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'usuarios.db')
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Inicializamos SQLAlchemy, Flask-Migrate y Bcrypt
db.init_app(app)  # Aquí inicializamos la base de datos después de cargar la configuración
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)




# Función para verificar si el usuario tiene el email de administrador
def es_usuario_administrador(email):
    # Buscamos el usuario por su email y verificamos si es administrador
    user = User.query.filter_by(email=email).first()
    if user and user.es_administrador:
        return True
    return False


# Página index.html
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Capturar los datos del formulario enviados por POST
        contacto_nombre = request.form.get('contacto_nombre')
        contacto_telefono = request.form.get('contacto_telefono')
        contacto_email = request.form.get('contacto_email')
        contacto_mensaje = request.form.get('contacto_mensaje')

        try:
            # Puedes guardar estos datos en la base de datos
            nuevo_contacto = User(
                contacto_nombre=contacto_nombre,
                contacto_telefono=contacto_telefono,
                contacto_email=contacto_email,
                contacto_mensaje=contacto_mensaje
            )

            db.session.add(nuevo_contacto)
            db.session.commit()

            # Flash para mostrar mensaje de éxito
            flash('Formulario enviado correctamente.')
        except Exception as e:
            flash(f'Ocurrió un error al enviar el formulario: {str(e)}')

        # Redirigir a la misma página principal después de enviar el formulario
        return redirect(url_for('index'))

    return render_template('index.html')


# Registro de usuarios
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Capturamos los datos del formulario
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        email = request.form['email']
        password = request.form['password']
        movil = request.form['movil']
        referido_por = request.form.get('referido_por', None)
        
        # Encriptamos la contraseña usando bcrypt
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Verificamos si el correo ya está registrado en la base de datos
        if User.query.filter_by(email=email).first():
            flash('Este correo ya está registrado')
            return redirect(url_for('register'))
        
        # Creamos un nuevo usuario
        new_user = User(
            nombre=nombre,
            apellidos=apellidos,
            email=email,
            password=hashed_password,
            movil=movil,
            referido_por=referido_por
        )

        # Asigna el campo es_administrador si es el correo de admin
        if email == 'Celiadiezdiaz98@gmail.com':
            new_user.es_administrador = True
        
        # Añadimos y confirmamos el usuario en la base de datos
        db.session.add(new_user)
        db.session.commit()
        
        flash('Usuario registrado exitosamente. Inicia sesión.')
        return redirect(url_for('login'))

    return render_template('register.html')

# Inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            
            user = User.query.filter_by(email=email).first()

            if user and bcrypt.check_password_hash(user.password, password):
                session['user_email'] = user.email
                session['user_id'] = user.id
                
                if user.es_administrador:
                    return redirect(url_for('supervision'))
                else:
                    return redirect(url_for('participa'))
            else:
                flash("Credenciales inválidas")
                return redirect(url_for('login'))

        return render_template('login.html')
    except Exception as e:
        # Log de errores para diagnóstico
        print("Error en la función login:", e)
        flash("Ocurrió un error durante el inicio de sesión.")
        return redirect(url_for('login'))



# Página de participación
@app.route('/participa')
def participa():
    if 'user_id' not in session:
        flash('Por favor, inicia sesión')
        return redirect(url_for('login'))
    return render_template('participa.html')


# Completar perfil
@app.route('/completarperfil', methods=['GET', 'POST'])
def completarperfil():
    if 'user_email' in session:
        user = User.query.filter_by(email=session['user_email']).first()

        if request.method == 'POST':
            # Capturar los datos del formulario
            edad = request.form.get('edad')
            movil = request.form.get('movil')
            motivo_crear_contenido = request.form.get('motivo_crear_contenido')
            tipo_contenido = request.form.get('tipo_contenido')
            tiempo_grabar = request.form.get('tiempo_grabar')
            motivacion = request.form.get('motivacion')
            conexion_audiencia = request.form.get('conexion_audiencia')
            

            try:
                # Actualizar el perfil del usuario con los nuevos datos
                user.edad = int(edad) if edad else user.edad
                user.movil = int(movil) if movil else user.movil
                user.motivo_crear_contenido = motivo_crear_contenido or user.motivo_crear_contenido
                user.tipo_contenido = tipo_contenido or user.tipo_contenido
                user.tiempo_grabar = tiempo_grabar or user.tiempo_grabar
                user.motivacion = motivacion or user.motivacion
                user.conexion_audiencia = conexion_audiencia or user.conexion_audiencia
                

                # Guardar cambios en la base de datos
                db.session.commit()

                # Flash para mostrar mensaje de éxito
                flash('Perfil completado correctamente.')
            except Exception as e:
                flash(f'Ocurrió un error al completar el perfil: {str(e)}')

        # Renderizar la página de completar perfil
        return render_template('completarperfil.html', user=user)

    else:
        flash('Por favor, inicia sesión.')
        return redirect(url_for('login'))



# Perfil de usuario
@app.route('/perfil', methods=['GET', 'POST'])
def perfil():
    if 'user_id' not in session:
        flash('Por favor, inicia sesión')
        return redirect(url_for('login'))
    
    user = User.query.filter_by(id=session['user_id']).first()

    if request.method == 'POST':
        user.youtube = request.form['youtube']
        user.instagram = request.form['instagram']
        user.tiktok = request.form['tiktok']
        user.twitch = request.form['twitch']
        db.session.commit()
        flash('Perfil actualizado')
        return redirect(url_for('perfil'))

    return render_template('perfil.html', usuario=user)

# Actualizar redes sociales de usuario
@app.route('/actualizar_redes_sociales/<int:user_id>', methods=['POST'])
def actualizar_redes_sociales(user_id):
    if 'user_id' not in session:
        flash('Por favor, inicia sesión')
        return redirect(url_for('login'))

    user = User.query.get_or_404(user_id)

    if user.id != session['user_id']:
        flash('No tienes permiso para actualizar este perfil')
        return redirect(url_for('supervision'))

    # Actualizar los campos de redes sociales
    user.youtube = request.form['youtube']
    user.instagram = request.form['instagram']
    user.tiktok = request.form['tiktok']
    user.twitch = request.form['twitch']
    db.session.commit()

    flash('Redes sociales actualizadas correctamente')
    return redirect(url_for('supervision'))


# Página de saldo
@app.route('/saldo')
def saldo():
    if 'user_id' not in session:
        flash('Por favor, inicia sesión')
        return redirect(url_for('login'))
    
    # Obtener el usuario autenticado desde la base de datos
    user = User.query.filter_by(id=session['user_id']).first()

    if not user:
        flash('Usuario no encontrado.')
        return redirect(url_for('login'))

    # Pasar el usuario a la plantilla para mostrar el saldo actualizado
    return render_template('saldo.html', usuario=user)

# Rutas adicionales para otrasformas
@app.route('/otrasformas')
def otrasformas():
    if 'user_id' not in session:
        flash('Por favor, inicia sesión')
        return redirect(url_for('login'))
    return render_template('otrasformas.html')

# Ruta para tiktok.html 
@app.route('/tiktok')
def tiktok():
    if 'user_id' not in session:
        flash('Por favor, inicia sesión')
        return redirect(url_for('login'))
    return render_template('tiktok.html')

#ACTUALIZAR REDES SOCIALES DE PERFIL.HTML 
@app.route('/update_social_media', methods=['POST'])
def update_social_media():
    if 'user_id' in session:  # Asegurarse de que el usuario esté autenticado
        user = User.query.get(session['user_id'])
        if user:
            # Actualizar redes sociales
            user.youtube = request.form.get('youtube')
            user.instagram = request.form.get('instagram')
            user.tiktok = request.form.get('tiktok')
            user.twitch = request.form.get('twitch')

            db.session.commit()
            flash("Redes sociales actualizadas correctamente", "success")
        else:
            flash("Usuario no encontrado", "danger")

    return redirect(url_for('perfil'))


# Ruta para el formulario de Corte de Borja
@app.route('/corte_de_borja', methods=['GET', 'POST'])
def corte_de_borja():
    if request.method == 'POST':
        user_id = session.get('user_id')  # Obtener el ID del usuario desde la sesión
        if user_id:
            # Procesa y guarda la participación
            # session[f'{user_id}_corte_de_borja_completado'] = True
            flash('Participación enviada correctamente en Corte de Borja.')  # Mensaje de éxito
            return redirect(url_for('corte_de_borja'))  # Redirige a la misma página
    return render_template('corte_de_borja.html')


# Ruta para el formulario de Vuela Libre
@app.route('/vuela_libre', methods=['GET', 'POST'])
def vuela_libre():
    if request.method == 'POST':
        user_id = session.get('user_id')
        if user_id:
            # Procesa y guarda la participación
            # session[f'{user_id}_vuela_libre_completado'] = True
            flash('Participación enviada correctamente en Vuela Libre.')
            return redirect(url_for('vuela_libre'))  # Redirige a la misma página
    return render_template('vuela_libre.html')


# Ruta para el formulario de Productores Loite
@app.route('/productores_loite', methods=['GET', 'POST'])
def productores_loite():
    if request.method == 'POST':
        user_id = session.get('user_id')
        if user_id:
            # Procesa y guarda la participación
            # session[f'{user_id}_productores_loite_completado'] = True
            flash('Participación enviada correctamente en Productores Loite.')
            return redirect(url_for('productores_loite'))  # Redirige a la misma página
    return render_template('productores_loite.html')



@app.route('/concursos')
def concursos():
    # Verificar si el usuario ha iniciado sesión
    if 'user_id' not in session:
        flash('Por favor, inicia sesión')
        return redirect(url_for('login'))
    
    # Si el usuario está autenticado, renderiza la página de concursos
    return render_template('concursos.html')


# Función para verificar si un usuario es administrador
def es_usuario_administrador(email):
    user = User.query.filter_by(email=email).first()
    return user and user.es_administrador


# Ruta de supervisión de usuarios
@app.route('/supervision', methods=['GET', 'POST'])
def supervision():
    # Verifica que el usuario tenga permiso para acceder a la supervisión
    if 'user_email' not in session or session['user_email'] != 'Celiadiezdiaz98@gmail.com':
        flash("No tienes permisos para acceder a esta página")
        return redirect(url_for('login'))

    # Actualizar saldo e historial de tareas si se envía el formulario
    if request.method == 'POST':
        user_id = request.form['user_id']
        saldo_nuevo = request.form['saldo']
        historial_tareas = request.form['historial_tareas']

        # Actualizar el usuario correspondiente en la base de datos
        usuario = User.query.get(user_id)
        if usuario:
            usuario.saldo = saldo_nuevo
            usuario.historial_tareas = historial_tareas
            db.session.commit()
            flash("Saldo y historial de tareas actualizados correctamente")
        else:
            flash("Usuario no encontrado")

    # Cargar todos los usuarios para mostrarlos en la página de supervisión
    usuarios = User.query.all()
    participaciones = Participacion.query.all()  # Obtén todas las participaciones
    return render_template('supervision.html', usuarios=usuarios , participaciones=participaciones)

    
@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    contacto_nombre = request.form.get('contacto_nombre')
    contacto_telefono = request.form.get('contacto_telefono')
    contacto_email = request.form.get('contacto_email')
    contacto_mensaje = request.form.get('contacto_mensaje')
    
    if not contacto_nombre or not contacto_telefono or not contacto_email or not contacto_mensaje:
        flash('Por favor, completa todos los campos del formulario.')
        return redirect(url_for('index'))

    nuevo_contacto = Contactos (contacto_nombre=contacto_nombre, contacto_telefono=contacto_telefono,
                              contacto_email=contacto_email, contacto_mensaje=contacto_mensaje)
    db.session.add(nuevo_contacto)
    db.session.commit()
    
    flash('Formulario enviado exitosamente')
    return redirect(url_for('index'))




@app.route('/formulariosupervision', methods=['GET', 'POST'])
def formulariosupervision():
    # Verificar si el usuario está autenticado y es administrador
    if 'user_email' in session:
        user = User.query.filter_by(email=session['user_email']).first()

        if user and user.es_administrador:
            # Obtener todos los contactos que se hayan registrado
            contactos = Contactos.query.filter(Contactos.contacto_nombre.isnot(None)).all()
            return render_template('formulariosupervision.html', contactos=contactos)
        else:
            flash('Acceso denegado. No tienes permisos de administrador.')
            return redirect(url_for('login'))
    else:
        flash('Por favor, inicia sesión.')
        return redirect(url_for('login'))


@app.route('/registro_participacion', methods=['POST'])
def registro_participacion():
    actividad = request.form.get('actividad')
    user_id = session.get('user_id')  # Obtener el user_id directamente desde la sesión

    # Verificar si user_id está en la sesión
    if not user_id:
        return "Error: user_id no proporcionado", 400

    participacion = Participacion.query.filter_by(user_id=user_id).first()
    if not participacion:
        participacion = Participacion(user_id=user_id)

    # Asigna el valor al campo correspondiente según la actividad
    if actividad == 'corte_de_borja':
        participacion.participacion_uno = request.form.get('participacion_uno')
    elif actividad == 'vuela_libre':
        participacion.participacion_dos = request.form.get('participacion_dos')
    elif actividad == 'productores_loite':
        participacion.participacion_tres = request.form.get('participacion_tres')

    db.session.add(participacion)
    db.session.commit()

    flash("¡Participación enviada correctamente!")

    return redirect(url_for('tiktok'))

@app.route('/link_a_condiciones')
def link_a_condiciones():
    return render_template('link_a_condiciones.html')

@app.route('/participacionesrecientes')
def participacionesrecientes():
    participaciones = Participacion.query.all()
    return render_template('participacionesrecientes.html', participaciones=participaciones)

@app.route('/guardar_notas', methods=['POST'])
def guardar_notas():
    user_id = request.form.get('user_id')
    mensaje = request.form.get('mensaje')
    
    # Obtén el usuario correspondiente
    usuario = User.query.get(user_id)
    if usuario:
        usuario.mensaje = mensaje  # Actualiza el campo de notas/mensaje
        db.session.commit()  # Guarda el cambio en la base de datos
        flash("Notas guardadas correctamente")
    else:
        flash("Usuario no encontrado")

    return redirect(url_for('supervision'))  # Redirige a la página de supervisión

@app.route('/asignar_codigo', methods=['POST'])
def asignar_codigo():
    user_id = request.form.get('user_id')
    valor_influencers = request.form.get('valor_influencers')
    
    # Obtén el usuario correspondiente
    usuario = User.query.get(user_id)
    if usuario:
        usuario.valor_influencers = valor_influencers  # Actualiza el valor del código de influencer
        db.session.commit()  # Guarda el cambio en la base de datos
        flash("Código asignado correctamente")
    else:
        flash("Usuario no encontrado")

    return redirect(url_for('supervision'))  # Redirige de nuevo a la página de supervisión

# Ruta para el aviso legal
@app.route('/avisolegal')
def avisolegal():
    return render_template('avisolegal.html')

# Solicita hablar con un agente
@app.route('/gestor', methods=['POST'])
def gestor():
    if 'user_id' not in session:
        flash('Por favor, inicia sesión')
        return redirect(url_for('login'))

    agent_request = AgentRequest(user_id=session['user_id'])
    db.session.add(agent_request)
    db.session.commit()
    flash('Solicitud enviada. Un agente se pondrá en contacto contigo.')
    return redirect(url_for('perfil'))

if __name__ == '__main__':
    app.run(debug=True)



