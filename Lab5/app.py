from flask import Flask, request, redirect, url_for, render_template_string
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

# Configure application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Important: Change this in a real application!

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Name of the login route

# In-memory user store (for demonstration purposes)
# In a real application, you would use a database
users_db = {
    "testuser": {"password": "password123"}
}

class User(UserMixin):
    def __init__(self, id):
        self.id = id

    @staticmethod
    def get(user_id):
        if user_id in users_db:
            return User(user_id)
        return None

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Routes
@app.route('/')
def index():
    return render_template_string('''
        <h1>Welcome!</h1>
        {% if current_user.is_authenticated %}
            <p>Hello, {{ current_user.id }}! <a href="{{ url_for('logout') }}">Logout</a></p>
            <p><a href="{{ url_for('protected') }}">Go to Protected Page</a></p>
        {% else %}
            <p><a href="{{ url_for('login') }}">Login</a></p>
        {% endif %}
    ''')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_data = users_db.get(username)
        if user_data and user_data['password'] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('protected'))
        return 'Invalid username or password'
    return render_template_string('''
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    ''')

@app.route('/protected')
@login_required
def protected():
    return render_template_string('''
        <h1>Protected Area</h1>
        <p>Hello, {{ current_user.id }}! This page is for authenticated users only.</p>
        <p><a href="{{ url_for('index') }}">Go to Home</a></p>
        <p><a href="{{ url_for('logout') }}">Logout</a></p>
    ''')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
