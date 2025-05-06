# Import necessary modules from Flask for web app development, routing, templating, requests, and error handling
from flask import Flask, redirect, url_for, render_template_string, request, abort
# Import Flask-Login for user session management (login, logout, current user, protected routes)
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
# Import Flask-Principal for role-based access control and permissions
from flask_principal import Principal, Identity, AnonymousIdentity, identity_changed, identity_loaded, RoleNeed, UserNeed, Permission


# Initialize the Flask application
app = Flask(__name__)
# Set a secret key for the application, used for session management and security.
# IMPORTANT: In a production environment, this should be a strong, random, and securely stored key.
app.secret_key = 'cualquier_cadena_segura'


# Configure Flask-Login
# Define the default view (route name) for login. Users will be redirected here if they try to access a protected page without being logged in.
default_login_view = 'login'
# Initialize the LoginManager with the Flask app
login_manager = LoginManager(app)
# Set the login view for the LoginManager
login_manager.login_view = default_login_view


# In-memory dictionary for test users. In a real application, this would typically be a database.
# Stores username, password, and roles for each user.
USERS = {
    'alice': {'password': '123', 'roles': ['admin']},
    'bob':   {'password': '456', 'roles': ['editor']},
}

# User class for Flask-Login. It needs to inherit from UserMixin for default implementations.

class User(UserMixin):
    # Constructor for the User class
    def __init__(self, username):
        # Set the user's ID (username)
        self.id = username
        # Retrieve and set the user's roles from the USERS dictionary
        self.roles = USERS[username]['roles']

# User loader function for Flask-Login. This function is called to reload the user object from the user ID stored in the session.

@login_manager.user_loader
def load_user(user_id):
    # Check if the user_id exists in our USERS dictionary
    if user_id in USERS:
        # If found, create and return a User object
        return User(user_id)
    # If not found, return None
    return None

# Configure Flask-Principal

# Configurar Flask-Principal
# Initialize Flask-Principal with the Flask app
principals = Principal(app)


# Define roles and permissions using Flask-Principal needs and permissions
# A 'Need' can be a RoleNeed (representing a role) or a UserNeed (representing a specific user).
# A 'Permission' is a collection of one or more needs.
# Define a 'Need' for the 'admin' role
admin_need  = RoleNeed('admin')
# Define a 'Need' for the 'editor' role
editor_need = RoleNeed('editor')


# Create a 'Permission' that requires the 'admin_need'
admin_permission  = Permission(admin_need)
# Create a 'Permission' that requires the 'editor_need'
editor_permission = Permission(editor_need)


# This function is connected to the 'identity_loaded' signal from Flask-Principal.
# It's called when a user's identity is established (e.g., after login).
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    # Set the user object on the identity
    identity.user = current_user
    # If the current user has an ID (is authenticated), add a UserNeed for this specific user
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))
    # For each role the current user has, add a RoleNeed to the identity
    # This tells Flask-Principal what roles the current identity possesses.
    for role in getattr(current_user, 'roles', []):
        identity.provides.add(RoleNeed(role))

# APPLICATION ROUTES
# Index page / Home page

@app.route('/')
def index():
    # Renders an HTML string template.
    # Shows user info and logout link if authenticated, or a login link if not.
    return render_template_string("""
      <h1>Welcome</h1>
      {% if current_user.is_authenticated %}
        <p>Hello {{ current_user.id }} (roles: {{ current_user.roles }})</p>
        <a href="{{ url_for('logout') }}">Logout</a>
      {% else %}
        <a href="{{ url_for('login') }}">Login</a>
      {% endif %}
    """ )

# Login page route, handles both GET (display form) and POST (process login) requests

@app.route('/login', methods=['GET','POST'])
def login():
    # If the request method is POST, try to log the user in
    if request.method == 'POST':
        # Get username and password from the submitted form
        u = request.form['username']
        p = request.form['password']
        # Check if username exists and password matches
        if u in USERS and USERS[u]['password'] == p:
            # Create a User object for the authenticated user
            user = User(u)
            # Log the user in using Flask-Login's login_user function
            login_user(user)
            # Signal Flask-Principal that the identity has changed (user logged in)
            identity_changed.send(app, identity=Identity(user.id))
            # Redirect to the index page after successful login
            return redirect(url_for('index'))
        # If authentication fails, return a 401 Unauthorized error
        return abort(401) # Unauthorized
    # If the request method is GET, display the login form
    return render_template_string("""
      <form method="post">
        <input name="username" placeholder="username"/><br>
        <input name="password" type="password" placeholder="password"/><br>
        <button type="submit">Login</button>
      </form>
    """ )

# Logout route

@app.route('/logout')
@login_required # Ensures only logged-in users can access this route
def logout():
    # Log the current user out using Flask-Login
    logout_user()
    # Signal Flask-Principal that the identity has changed to an anonymous one
    identity_changed.send(app, identity=AnonymousIdentity())
    # Redirect to the index page after logout
    return redirect(url_for('index'))

@app.route('/admin')
@login_required # Requires user to be logged in
@admin_permission.require(http_exception=403) # Requires admin role, returns 403 Forbidden if not met
def admin_page():
    # Content for the admin page
    return '<h2>Admin Zone</h2>'

# Editor page route, protected by login and editor permission

@app.route('/editor')
@login_required # Requires user to be logged in
@editor_permission.require(http_exception=403) # Requires editor role, returns 403 Forbidden if not met
def editor_page():
    # Content for the editor page
    return '<h2>Editor Zone</h2>'

# Shared page route, accessible to any logged-in user

@app.route('/shared')
@login_required # Requires user to be logged in, but no specific role beyond authentication
def shared_page():
    # Content for the shared page
    return '<h2>Page accessible to any logged-in user</h2>'

# Main execution block: runs the Flask development server if the script is executed directly.

if __name__ == '__main__':
    # Run the app with debug mode enabled. 
    # Debug mode should be turned OFF in a production environment.
    app.run(debug=True)
