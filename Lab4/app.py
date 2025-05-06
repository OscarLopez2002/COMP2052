<<<<<<< HEAD
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
=======
# Necessary imports from Flask and the form
from flask import Flask, render_template, flash, redirect, url_for
from forms import RegistrationForm # Import the RegistrationForm class from forms.py

# Create an instance of the Flask application
app = Flask(__name__)

# Configure a secret key for the application.
# This is crucial for session security and WTForms CSRF protection.
# In a production environment, this key should be a random, secure value and not hardcoded.
app.config['SECRET_KEY'] = 'my_super_secret_and_secure_key_123' # Changed to English and kept generic

# Define the route for the registration page
# Accepts GET (to display the form) and POST (to submit form data) methods
@app.route('/register', methods=['GET', 'POST']) # Changed route to /register
def register(): # Changed function name to register
    # Create an instance of the registration form
    form = RegistrationForm()
    
    # validate_on_submit() checks if the form was submitted (POST) and if all validators passed
    if form.validate_on_submit():
        # If the form is valid, extract the data
        name = form.name.data # Changed to form.name.data
        email = form.email.data # Changed to form.email.data
        password = form.password.data # Changed to form.password.data. Important! In a real application, hash this password before saving.
        
        # Here you would add logic to process the data (e.g., save to a database)
        # For now, we just show a success flash message
        flash(f'Account created successfully for {name}! Email: {email}', 'success') # Message in English
        
        # Redirect the user to another page (e.g., a login page or a dashboard)
        # We use url_for to dynamically generate the URL from the view function's name.
        return redirect(url_for('example_page')) # Changed to example_page
    
    # If the method is GET or the form is not valid (validation errors),
    # render the registration HTML template, passing the form as context.
    return render_template('register.html', title='User Registration', form=form) # title in English, template name kept as registro.html for now

# An example route to redirect to after successful registration
@app.route('/example_page') # Changed route to /example_page
def example_page(): # Changed function name to example_page
    return "<h1>Welcome!</h1><p>This is a page you are redirected to after successful registration.</p><a href='/register'>Back to registration</a>" # Content in English, link to /register

# Entry point to run the Flask application
# The if __name__ == '__main__': conditional ensures that the development server
# only runs when the script is executed directly (not when imported as a module).
if __name__ == '__main__':
    # app.run() starts the Flask development server.
    # debug=True enables debug mode, which provides useful error information
    # and automatically reloads the server when code changes are detected.
    # Do not use debug=True in a production environment!
>>>>>>> 0176ce9 (Update files and remove nested .git folders)
    app.run(debug=True)
