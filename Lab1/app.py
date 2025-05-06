# Importamos las clases necesarias de Flask: Flask para crear la aplicación,
# request para acceder a los datos de las solicitudes entrantes (como JSON),
# y jsonify para convertir diccionarios de Python a respuestas JSON.
from flask import Flask, request, jsonify # type: ignore

# Creamos una instancia de la aplicación Flask.
# __name__ es una variable especial en Python que representa el nombre del módulo actual.
# Flask lo usa para localizar recursos como plantillas y archivos estáticos.
app = Flask(__name__)

# Definimos una ruta para la URL '/info' que solo acepta peticiones GET.
# El decorador @app.route() asocia la función 'info()' con esta URL y método.
@app.route('/info', methods=['GET'])
# Esta función se ejecuta cuando se accede a '/info' con un método GET.
def info():
    return jsonify({
        'app': 'Mi Aplicación Flask',
        'version': '1.0.0',
        'author': 'OSCAR'
    })

# Definimos una ruta para la URL '/mensaje' que solo acepta peticiones POST.
@app.route('/mensaje', methods=['POST'])
# Esta función se ejecuta cuando se accede a '/mensaje' con un método POST.
def mensaje():
    # Obtenemos los datos enviados en el cuerpo de la petición POST, asumiendo que es JSON.
    data = request.get_json()
    # Verificamos si se enviaron datos y si el campo 'mensaje' está presente en el JSON.
    if not data or 'mensaje' not in data:
        # Si no se cumplen las condiciones, devolvemos un error 400 (Bad Request).
        return jsonify({'error': 'Falta el campo "mensaje" en el JSON'}), 400
    # Extraemos el valor del campo 'mensaje' del JSON recibido.
    contenido = data['mensaje']
    # Creamos una respuesta personalizada utilizando el contenido del mensaje.
    respuesta = f'Recibido: {contenido}'
    # Devolvemos la respuesta personalizada en formato JSON.
    return jsonify({'respuesta': respuesta})

# Definimos una ruta para la URL raíz '/' que solo acepta peticiones GET.
@app.route('/', methods=['GET'])
# Esta función se ejecuta cuando se accede a la URL raíz '/'.
def home():
    # Devolvemos una cadena de texto que contiene HTML para renderizar una página web básica.
    return """<!DOCTYPE html>
<html>
<head>
    <title>Bienvenido</title>
    <style>
        body {
            font-family: sans-serif;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background-color: #f0f0f0;
        }
        .container {
            text-align: center;
            padding: 2em;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Bienvenido a mi API</h1>
    </div>
</body>
</html>"""

# Este bloque se ejecuta solo si el script se corre directamente (no si se importa como módulo).
if __name__ == '__main__':
    # Iniciamos el servidor de desarrollo de Flask.
    # debug=True activa el modo de depuración, que reinicia automáticamente el servidor
    # cuando detecta cambios en el código y proporciona mensajes de error detallados.
    app.run(debug=True)