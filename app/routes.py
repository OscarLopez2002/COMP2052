from flask import Blueprint, render_template, flash, redirect, url_for, request
from .forms import RegistrationForm

bp = Blueprint('main', __name__)

# Datos de ejemplo
PRODUCTOS = [
    {'id': 1, 'nombre': 'Cámara',     'precio': 299},
    {'id': 2, 'nombre': 'Teléfono',   'precio': 499},
    {'id': 3, 'nombre': 'Auriculares','precio': 59},
]
USUARIOS = ['Ana', 'Luis', 'María', 'Pedro']

@bp.route('/')
def inicio():
    return render_template('index.html')

@bp.route('/productos')
def lista_productos():
    return render_template('productos.html', productos=PRODUCTOS)

@bp.route('/usuarios')
def lista_usuarios():
    return render_template('usuarios.html', usuarios=USUARIOS)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Aquí iría lógica de registro (db, etc.)
        flash(f"Usuario {form.name.data} registrado con éxito!", 'success')
        return redirect(url_for('main.inicio'))
    return render_template('register.html', form=form)
