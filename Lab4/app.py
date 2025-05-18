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

@app.route('/')
def home_page():
    return redirect(url_for('register'))

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
    app.run(debug=True)
