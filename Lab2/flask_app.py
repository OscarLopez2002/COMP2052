<<<<<<< HEAD
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
=======
# Import necessary modules from Flask: Flask for creating the application instance,
# request for accessing incoming request data (e.g., JSON payloads),
# jsonify for converting Python dictionaries to JSON responses,
# render_template for rendering HTML templates.
from flask import Flask, request, jsonify, render_template

# Create an instance of the Flask class.
# __name__ is a special Python variable that gets the name of the current module.
# Flask uses this to know where to look for templates, static files, etc.
app = Flask(__name__)

# In-memory list to store user data.
# In a production application, you would typically use a database for persistent storage.
usuarios = []

# Define a route for GET requests to /info.
# This route returns general information about the system.
@app.route('/info', methods=['GET'])
def obtener_info():
    # Create a Python dictionary containing system information.
    info = {
        'nombre_sistema': 'Sistema de Gestión de Usuarios',
        'version': '1.0',
        'autor': 'Tu Nombre', # You can replace 'Tu Nombre' with your actual name.
        'descripcion': 'Este sistema permite gestionar usuarios mediante rutas en Flask'
    }
    # Convert the dictionary to a JSON response.
    return jsonify(info)

# Define a route for POST requests to /crear_usuario.
# This route handles the creation of new users.
@app.route('/crear_usuario', methods=['POST'])
def crear_usuario():
    # Get the JSON data sent in the request body.
    datos = request.get_json()

    # Validate that data was sent.
    if not datos:
        # If no data is sent, return an error response with HTTP status code 400 (Bad Request).
        return jsonify({'error': 'No se enviaron datos'}), 400

    # Extract 'nombre' (name) and 'correo' (email) from the received data.
    nombre = datos.get('nombre')
    correo = datos.get('correo')

    # Validate that both 'nombre' and 'correo' are present.
    if not nombre or not correo:
        # If either is missing, return an error response with HTTP status code 400.
        return jsonify({'error': 'El nombre y el correo son obligatorios'}), 400

    # Create a dictionary representing the new user.
    usuario = {'nombre': nombre, 'correo': correo}
    # Add the new user to the in-memory list.
    usuarios.append(usuario)
    # Return a success message and the created user data with HTTP status code 201 (Created).
    return jsonify({'mensaje': 'Usuario creado exitosamente', 'usuario': usuario}), 201

# Define a route for GET requests to /usuarios.
# This route returns the list of all stored users.
@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    # Return the list of users as a JSON response.
    return jsonify({'usuarios': usuarios})

# Define a route for GET requests to the root URL (/).
# This route serves the main HTML page.
@app.route('/', methods=['GET'])
def index():
    # Render the 'index.html' template.
    # Pass the current list of 'usuarios' to the template so it can be displayed.
    return render_template('index.html', usuarios=usuarios)

# This block ensures that the Flask development server runs only when the script is executed directly
# (not when it's imported as a module into another script).
if __name__ == '__main__':
    # Start the Flask development server.
    # debug=True enables debug mode, which provides helpful error messages and auto-reloads the server on code changes.
>>>>>>> 0176ce9 (Update files and remove nested .git folders)
    app.run(debug=True)