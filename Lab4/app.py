from flask import Flask, redirect, url_for, render_template_string, request, abort
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from flask_principal import Principal, Identity, AnonymousIdentity, identity_changed, identity_loaded, RoleNeed, UserNeed, Permission

app = Flask(__name__)
app.secret_key = 'cualquier_cadena_segura'

# Configurar LoginManager
default_login_view = 'login'
login_manager = LoginManager(app)
login_manager.login_view = default_login_view

# Usuarios de prueba
USERS = {
    'alice': {'password': '123', 'roles': ['admin']},
    'bob':   {'password': '456', 'roles': ['editor']},
}

class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.roles = USERS[username]['roles']

@login_manager.user_loader
def load_user(user_id):
    if user_id in USERS:
        return User(user_id)
    return None

# Configurar Flask-Principal
principals = Principal(app)

# Definir roles y permisos
admin_need  = RoleNeed('admin')
editor_need = RoleNeed('editor')

admin_permission  = Permission(admin_need)
editor_permission = Permission(editor_need)

# Cargar identidad tras cambios de login/logout
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    identity.user = current_user
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))
    for role in getattr(current_user, 'roles', []):
        identity.provides.add(RoleNeed(role))

# RUTAS DE LA APP
@app.route('/')
def index():
    return render_template_string("""
      <h1>Bienvenido</h1>
      {% if current_user.is_authenticated %}
        <p>Hola {{ current_user.id }} (roles: {{ current_user.roles }})</p>
        <a href="{{ url_for('logout') }}">Logout</a>
      {% else %}
        <a href="{{ url_for('login') }}">Login</a>
      {% endif %}
    """ )

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        if u in USERS and USERS[u]['password'] == p:
            user = User(u)
            login_user(user)
            identity_changed.send(app, identity=Identity(user.id))
            return redirect(url_for('index'))
        return abort(401)
    return render_template_string("""
      <form method="post">
        <input name="username" placeholder="user"/><br>
        <input name="password" type="password"/><br>
        <button>Login</button>
      </form>
    """ )

@app.route('/logout')
@login_required
def logout():
    logout_user()
    identity_changed.send(app, identity=AnonymousIdentity())
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
@admin_permission.require(http_exception=403)
def admin_page():
    return '<h2>Zona Admin</h2>'

@app.route('/editor')
@login_required
@editor_permission.require(http_exception=403)
def editor_page():
    return '<h2>Zona Editor</h2>'

@app.route('/shared')
@login_required
def shared_page():
    return '<h2>Página accesible para cualquier usuario logueado</h2>'

if __name__ == '__main__':
    app.run(debug=True)
