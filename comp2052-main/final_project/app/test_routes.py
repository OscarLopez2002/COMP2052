from flask import Blueprint, request, jsonify
from app.models import db, Encuesta

# Blueprint solo con endpoints de prueba para encuestas
test_main = Blueprint('test_main', __name__, url_prefix='/test') # Added url_prefix for namespacing

@test_main.route('/')
@test_main.route('/dashboard')
def index_test():
    """
    Página de inicio pública (home) para pruebas.
    """
    return '<h1>Corriendo en Modo de Prueba (Encuestas).</h1>'

@test_main.route('/encuestas', methods=['GET'])
def listar_encuestas():
    """
    Retorna una lista de encuestas (JSON).
    """
    encuestas = Encuesta.query.all()

    data = [
        {'id': encuesta.id, 'titulo': encuesta.titulo, 'descripcion': encuesta.descripcion, 'creador_id': encuesta.creador_id}
        for encuesta in encuestas
    ]
    return jsonify(data), 200


@test_main.route('/encuestas/<int:id>', methods=['GET'])
def listar_un_encuesta(id):
    """
    Retorna una sola encuesta por su ID (JSON).
    """
    encuesta = Encuesta.query.get_or_404(id)

    data = {
        'id': encuesta.id,
        'titulo': encuesta.titulo,
        'descripcion': encuesta.descripcion,
        'creador_id': encuesta.creador_id
    }

    return jsonify(data), 200


@test_main.route('/encuestas', methods=['POST'])
def crear_encuesta():
    """
    Crea una encuesta sin validación.
    Espera JSON con 'titulo', 'descripcion' y 'creador_id'.
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    encuesta = Encuesta(
        titulo=data.get('titulo'),
        descripcion=data.get('descripcion'),
        creador_id=data.get('creador_id')  # sin validación de usuario
    )

    db.session.add(encuesta)
    db.session.commit()

    return jsonify({'message': 'Encuesta creada', 'id': encuesta.id, 'creador_id': encuesta.creador_id}), 201

@test_main.route('/encuestas/<int:id>', methods=['PUT'])
def actualizar_encuesta(id):
    """
    Actualiza una encuesta sin validación de usuario o permisos.
    """
    encuesta = Encuesta.query.get_or_404(id)
    data = request.get_json()

    encuesta.titulo = data.get('titulo', encuesta.titulo)
    encuesta.descripcion = data.get('descripcion', encuesta.descripcion)
    encuesta.creador_id = data.get('creador_id', encuesta.creador_id)

    db.session.commit()

    return jsonify({'message': 'Encuesta actualizada', 'id': encuesta.id}), 200

@test_main.route('/encuestas/<int:id>', methods=['DELETE'])
def eliminar_encuesta(id):
    """
    Elimina una encuesta sin validación de permisos.
    """
    encuesta = Encuesta.query.get_or_404(id)
    db.session.delete(encuesta)
    db.session.commit()

    return jsonify({'message': 'Encuesta eliminada', 'id': encuesta.id}), 200
