from flask import Flask, render_template

app = Flask(__name__)

# Datos de ejemplo
PRODUCTOS = [
    {'id': 1, 'nombre': 'Cámara',     'precio': 299},
    {'id': 2, 'nombre': 'Teléfono',   'precio': 499},
    {'id': 3, 'nombre': 'Auriculares','precio': 59},
]
USUARIOS = ['Ana', 'Luis', 'María', 'Pedro']

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/productos')
def productos():
    return render_template('productos.html', productos=PRODUCTOS)

@app.route('/usuarios')
def usuarios():
    return render_template('usuarios.html', usuarios=USUARIOS)

if __name__ == '__main__':
    app.run(debug=True)
