from flask import Flask, request, jsonify # type: ignore

app = Flask(__name__)

@app.route('/info', methods=['GET'])
def info():
    return jsonify({
        'app': 'Mi Aplicación Flask',
        'version': '1.0.0',
        'author': 'OSCAR'
    })

@app.route('/mensaje', methods=['POST'])
def mensaje():
    data = request.get_json()
    if not data or 'mensaje' not in data:
        return jsonify({'error': 'Falta el campo "mensaje" en el JSON'}), 400
    contenido = data['mensaje']
    respuesta = f'Recibido: {contenido}'
    return jsonify({'respuesta': respuesta})

@app.route('/', methods=['GET'])
def home():
    return jsonify({'msg':'Bienvenido a mi API'})

if __name__ == '__main__':
    app.run(debug=True)