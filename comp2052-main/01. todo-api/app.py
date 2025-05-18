from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Base de datos simulada en memoria
todos = {
    "todos": ['Study for the English course', 
              'Mowing the Patio', 
              'Go to the beach on Sunday']
}

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", data=todos, message=None)

@app.route("/todos", methods=["GET"])
def select_todos():
    """
    Obtener todos los TODOs.
    Retorna un JSON con la lista actual de tareas.
    """
    return jsonify(todos)

@app.route("/todos", methods=["POST"])
def create_todo():
    """
    Crear un nuevo TODO.
    Espera un JSON con el campo 'todo'.
    """
    data = request.json
    todo_item = data.get('todo')
    if not todo_item:
        return jsonify({"error": "Datos incompletos"}), 400

    todos["todos"].append(todo_item)
    return jsonify({"message": "Nuevo TODO creado"}), 201

@app.route("/todos", methods=["DELETE"])
def delete_todo():
    """
    Eliminar un TODO existente.
    Espera un JSON con el campo 'todo' que debe coincidir exactamente.
    """
    data = request.json
    todo_item = data.get('todo')
    if not todo_item:
        return jsonify({"error": "Datos incompletos"}), 400

    if todo_item not in todos["todos"]:
        return jsonify({"error": "TODO NO encontrado"}), 404

    todos["todos"].remove(todo_item)
    return jsonify({"message": f"TODO '{todo_item}' eliminado"}), 200

@app.route("/todos", methods=["PUT"])
def update_todo():
    """
    Actualizar un TODO existente.
    Espera un JSON con los campos 'old' y 'new'.
    """
    data = request.json
    old_todo = data.get('old')
    new_todo = data.get('new')

    if not old_todo or not new_todo:
        return jsonify({"error": "Datos incompletos"}), 400

    if old_todo not in todos["todos"]:
        return jsonify({"error": "TODO no encontrado"}), 404

    index = todos["todos"].index(old_todo)
    todos["todos"][index] = new_todo

    return jsonify({"message": f"TODO actualizado de '{old_todo}' a '{new_todo}'"}), 200

if __name__ == "__main__":
    app.run(debug=True)
