from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.forms import EncuestaForm, ChangePasswordForm
from app.models import db, Encuesta, User, Role # Added Role

# Blueprint principal que maneja el dashboard, gestión de encuestas y cambio de contraseña
main = Blueprint('main', __name__)

@main.route('/')
def index():
    """
    Página de inicio pública (home).
    """
    return render_template('index.html')

@main.route('/cambiar-password', methods=['GET', 'POST'])
@login_required
def cambiar_password():
    """
    Permite al usuario autenticado cambiar su contraseña.
    """
    form = ChangePasswordForm()

    if form.validate_on_submit():
        # Verifica que la contraseña actual sea correcta
        if not current_user.check_password(form.old_password.data):
            flash('Current password is incorrect.')  # 🔁 Traducido
            return render_template('cambiar_password.html', form=form)

        # Actualiza la contraseña y guarda
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('✅ Password updated successfully.')  # 🔁 Traducido
        return redirect(url_for('main.dashboard'))

    return render_template('cambiar_password.html', form=form)

@main.route('/dashboard')
@login_required
def dashboard():
    """
    Panel principal del usuario. Muestra las encuestas.
    """
    encuestas_list = [] # Renamed to avoid conflict with imported Encuesta model
    if current_user.role.name == 'Admin':
        encuestas_list = Encuesta.query.all()  # Admin ve todas las encuestas
    elif current_user.role.name == 'Moderador':
        # Moderador ve las encuestas que ha creado
        encuestas_list = Encuesta.query.filter_by(creador_id=current_user.id).all()
    elif current_user.role.name == 'Votante':
        # Votante ve todas las encuestas (podría filtrarse por activas en el futuro)
        encuestas_list = Encuesta.query.all()
    # Considerar otros roles o usuarios sin un rol específico si es necesario

    return render_template('dashboard.html', encuestas=encuestas_list, current_user_role=current_user.role.name)

@main.route('/encuestas', methods=['GET', 'POST'])
@login_required
def encuestas():
    """
    Permite crear una nueva encuesta. Solo disponible para Moderadores o Admins.
    """
    if current_user.role.name not in ['Admin', 'Moderador']:
        flash('No tienes permiso para crear encuestas.')
        return redirect(url_for('main.dashboard'))

    form = EncuestaForm()
    if form.validate_on_submit():
        encuesta = Encuesta(
            titulo=form.titulo.data,
            descripcion=form.descripcion.data,
            creador_id=current_user.id
        )
        db.session.add(encuesta)
        db.session.commit()
        flash("Encuesta creada exitosamente.")
        return redirect(url_for('main.dashboard'))

    return render_template('encuesta_form.html', form=form, title="Crear Encuesta")

@main.route('/encuestas/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_encuesta(id):
    """
    Permite editar una encuesta existente. Solo si es Admin o el Moderador dueño.
    """
    encuesta = Encuesta.query.get_or_404(id)

    # Validación de permisos
    if not (current_user.role.name == 'Admin' or (current_user.role.name == 'Moderador' and encuesta.creador_id == current_user.id)):
        flash('No tienes permiso para editar esta encuesta.')
        return redirect(url_for('main.dashboard'))

    form = EncuestaForm(obj=encuesta)

    if form.validate_on_submit():
        encuesta.titulo = form.titulo.data
        encuesta.descripcion = form.descripcion.data
        db.session.commit()
        flash("Encuesta actualizada exitosamente.")
        return redirect(url_for('main.dashboard'))

    return render_template('encuesta_form.html', form=form, encuesta=encuesta, title="Editar Encuesta", editar=True)

@main.route('/encuestas/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_encuesta(id):
    """
    Elimina una encuesta si el usuario es Admin o el Moderador creador.
    """
    encuesta = Encuesta.query.get_or_404(id)

    if not (current_user.role.name == 'Admin' or (current_user.role.name == 'Moderador' and encuesta.creador_id == current_user.id)):
        flash('No tienes permiso para eliminar esta encuesta.')
        return redirect(url_for('main.dashboard'))

    # Aquí podrías añadir lógica para eliminar preguntas, opciones y votos asociados si es necesario
    # Por ejemplo: Voto.query.filter_by(encuesta_id=id).delete()
    # Pregunta.query.filter_by(encuesta_id=id).delete() # y sus opciones

    db.session.delete(encuesta)
    db.session.commit()
    flash("Encuesta eliminada exitosamente.")
    return redirect(url_for('main.dashboard'))

@main.route('/usuarios')
@login_required
def listar_usuarios():
    if current_user.role.name != 'Admin':
        flash("You do not have permission to view this page.")
        return redirect(url_for('main.dashboard'))

    # Obtener instancias completas de usuarios con sus roles (no usar .add_columns)
    usuarios = User.query.join(User.role).all()

    return render_template('usuarios.html', usuarios=usuarios)
