from flask import Flask, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)

app.secret_key = "clave_secreta"

login_manager = LoginManager(app)
login_manager.login_view = "login"

# Modelo de usuario
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

# Datos de ejemplo
users = {
    "juan": User(1, "juan"), 
    "maria": User(2, "maria")
    }

@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if str(user.id) == user_id:
            return user
    return None

@app.route("/login/<username>")
def login(username):
    user = users.get(username)
    if user:
        login_user(user)
        return f"Bienvenido {current_user.username}!"
    else:
        return "Usuario no encontrado", 404

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return "Sesión cerrada"

@app.route("/dashboard")
@login_required
def dashboard():
    return f"Hola, {current_user.username}! Bienvenido a tu Home Page."

if __name__ == "__main__":
    app.run(debug=True)