from flask import Flask, request, jsonify

app = Flask(__name__)

# Lista para almacenar los usuarios en memoria
usuarios = []

# Ruta GET /info
@app.route('/info', methods=['GET'])
def obtener_info():
    return jsonify({
        'nombre_sistema': 'Sistema de Gestión de Usuarios',
        'version': '1.0',
        'autor': 'Tu Nombre',
        'descripcion': 'Este sistema permite gestionar usuarios mediante rutas en Flask'
    })

# Ruta POST /crear_usuario
@app.route('/crear_usuario', methods=['POST'])
def crear_usuario():
    datos = request.get_json()
    if not datos:
        return jsonify({'error': 'No se enviaron datos'}), 400

    nombre = datos.get('nombre')
    correo = datos.get('correo')

    if not nombre or not correo:
        return jsonify({'error': 'El nombre y el correo son obligatorios'}), 400

    usuario = {'nombre': nombre, 'correo': correo}
    usuarios.append(usuario)
    return jsonify({'mensaje': 'Usuario creado exitosamente', 'usuario': usuario}), 201

# Ruta GET /usuarios
@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    return jsonify({'usuarios': usuarios})

if __name__ == '__main__':
    app.run(debug=True)