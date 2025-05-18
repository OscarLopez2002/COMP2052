# Import necessary modules from Flask: Flask for creating the app, request for handling HTTP requests, jsonify for returning JSON responses, and render_template for serving HTML files.
from flask import Flask, request, jsonify, render_template # type: ignore

# Create a Flask application instance.
app = Flask(__name__)

# Define a route for '/info' that accepts GET requests.
@app.route('/info', methods=['GET'])
def info():
    # Application information
    app_info = {
        'app': 'Mi Aplicación Flask',
        'version': '1.0.0',
        'author': 'OSCAR'
    }
    # Render an HTML page displaying the application information.
    return render_template('info.html', info=app_info)

# Define a route for '/mensaje' that accepts POST requests.
@app.route('/mensaje', methods=['POST'])
def mensaje():
    # Get JSON data from the request.
    data = request.get_json()
    # Check if data is present and contains the 'mensaje' field.
    if not data or 'mensaje' not in data:
        # Return an error response if 'mensaje' is missing.
        return jsonify({'error': 'Falta el campo "mensaje" en el JSON'}), 400
    # Extract the 'mensaje' content from the data.
    contenido = data['mensaje']
    # Create a response string.
    respuesta = f'Recibido: {contenido}'
    # Return a JSON response with the received message.
    return jsonify({'respuesta': respuesta})

# Define a route for the root URL '/' that accepts GET requests.
@app.route('/', methods=['GET'])
def home():
    # Render the main HTML page.
    return render_template('index.html')

# Check if the script is executed directly (not imported).
if __name__ == '__main__':
    # Run the Flask development server with debug mode enabled.
    app.run(debug=True)
