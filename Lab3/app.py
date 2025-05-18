# Import necessary modules from Flask for web application functionalities
from flask import Flask, render_template, redirect, url_for, request, flash
# Import SQLAlchemy for database interactions
from flask_sqlalchemy import SQLAlchemy
# Import Flask-Login for user session management (login, logout, protected routes)
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
# Import functions for password hashing and checking from Werkzeug
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize the Flask application
app = Flask(__name__)
# Configure a secret key for session management and other security purposes (IMPORTANT: change this in a production environment)
app.config['SECRET_KEY'] = 'changeThisSecretKey'
# Configure the SQLAlchemy database URI to use an SQLite database named 'users.db' in the instance folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# Disable SQLAlchemy event tracking to save resources, as it's often not needed and can add overhead
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the Flask app to enable database operations
db = SQLAlchemy(app)
# Initialize the LoginManager for handling user authentication and session management
login_manager = LoginManager()
# Specify the route name for the login page. Flask-Login will redirect users to this page if they try to access a protected route without being logged in.
login_manager.login_view = 'login'
# Initialize the LoginManager with the Flask app to integrate it with the application
login_manager.init_app(app)

# Define the User model for the database
# Inherits from UserMixin to provide default implementations for Flask-Login (e.g., is_authenticated, is_active)
# Inherits from db.Model to make it an SQLAlchemy model
class User(UserMixin, db.Model):
    # Define the 'id' column: an integer that serves as the primary key for the table
    id = db.Column(db.Integer, primary_key=True)
    # Define the 'username' column: a string with a maximum length of 150 characters, must be unique across all users
    username = db.Column(db.String(150), unique=True, nullable=False) # Added nullable=False for data integrity
    # Define the 'password' column: a string with a maximum length of 150 characters, storing the hashed password
    password = db.Column(db.String(150), nullable=False) # Added nullable=False for data integrity

# User loader function required by Flask-Login
# This function is called to reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(user_id):
    # Retrieve a user from the database by their integer ID
    return User.query.get(int(user_id))

# Function to create database tables before the first request
# This ensures that the database schema is set up when the application starts
@app.before_first_request
def create_tables():
    # Create all database tables defined in the SQLAlchemy models (i.e., the User table here)
    db.create_all()

# Route for the home page ('/')
# This is the main landing page of the application
@app.route('/')
def home():
    # Render the 'home.html' template
    return render_template('home.html')

# Route for the login page ('/login')
# Accepts both GET (to display the form) and POST (to process the form) requests
@app.route('/login', methods=['GET','POST'])
def login():
    # If the request method is POST, it means the user submitted the login form
    if request.method == 'POST':
        # Get the username from the submitted form data
        username = request.form.get('username')
        # Get the password from the submitted form data
        password = request.form.get('password')
        # Query the database for a user with the provided username
        user = User.query.filter_by(username=username).first()
        
        # Check if the user exists and if the provided password matches the stored hashed password
        if not user or not check_password_hash(user.password, password):
            # If credentials are invalid, flash an error message to be displayed on the page
            flash('Invalid credentials. Please try again.')
            # Redirect the user back to the login page
            return redirect(url_for('login'))
            
        # If credentials are valid, log in the user using Flask-Login's login_user function
        login_user(user)
        # Flash a success message
        flash('Logged in successfully!')
        # Redirect the logged-in user to the 'protected' page (or a dashboard, etc.)
        return redirect(url_for('protected'))
        
    # If the request method is GET, simply render the 'login.html' template to display the form
    return render_template('login.html')

# Route for the registration page ('/register')
# Accepts both GET (to display the form) and POST (to process the form) requests
@app.route('/register', methods=['GET','POST'])
def register():
    # If the request method is POST, it means the user submitted the registration form
    if request.method == 'POST':
        # Get the username from the submitted form data
        username = request.form.get('username')
        # Get the password from the submitted form data
        password = request.form.get('password')
        
        # Check if a user with the given username already exists in the database
        if User.query.filter_by(username=username).first():
            # If the user already exists, flash an error message
            flash('Username already exists. Please choose a different one.')
            # Redirect the user back to the registration page
            return redirect(url_for('register'))
            
        # If the username is available, create a new User object
        # Hash the password using generate_password_hash for security. 'pbkdf2:sha256' is a common secure method.
        new_user = User(username=username,
                        password=generate_password_hash(password, method='pbkdf2:sha256')) # Changed method to pbkdf2:sha256 for better security
                        
        # Add the new user object to the database session
        db.session.add(new_user)
        # Commit the session to save the new user to the database
        db.session.commit()
        
        # Flash a success message indicating that the user has been created
        flash('User created successfully! Please log in.')
        # Redirect the user to the login page
        return redirect(url_for('login'))
        
    # If the request method is GET, render the 'register.html' template to display the form
    return render_template('register.html')

# Route for a protected page ('/protected')
# This page requires the user to be logged in
@app.route('/protected')
@login_required # Flask-Login decorator: ensures only authenticated users can access this route
def protected():
    # Render the 'protected.html' template
    # Pass the current logged-in user's username to the template for display
    return render_template('protected.html', name=current_user.username)

# Route for logging out ('/logout')
@app.route('/logout')
@login_required # Ensures only authenticated users can attempt to log out
def logout():
    # Log out the current user using Flask-Login's logout_user function
    logout_user()
    # Flash a message confirming logout
    flash('You have been logged out.')
    # Redirect the user to the home page
    return redirect(url_for('home'))

# Standard Python entry point:
# This block ensures that the Flask development server is run only when the script is executed directly
# (not when it's imported as a module).
if __name__=='__main__':
    # Run the Flask app with debug mode enabled.
    # Debug mode provides helpful error messages and reloads the server on code changes during development.
    # IMPORTANT: Debug mode should be turned OFF in a production environment.
    app.run(debug=True)
