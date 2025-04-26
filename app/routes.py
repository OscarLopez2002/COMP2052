from flask import Blueprint, render_template

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
