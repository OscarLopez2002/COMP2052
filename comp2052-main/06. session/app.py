from flask import Flask, session

app = Flask(__name__)

app.secret_key = "clave_secreta"

@app.route("/login")
def login():
    session["usuario"] = "Juan"
    return "Usuario autenticado"

@app.route("/user")
def get_user():
    usuario = session.get("usuario")
    if usuario:
        return f"Usuario registrado: {usuario}"
    else:
        return "Sesión NO registrada"

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return "Sesión cerrada"

if __name__ == "__main__":
    app.run(debug=True)