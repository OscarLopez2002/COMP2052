# Import FlaskForm for creating forms
from flask_wtf import FlaskForm
# Import field types (StringField, PasswordField, SubmitField)
from wtforms import StringField, PasswordField, SubmitField
# Import validators (DataRequired, Email, Length)
from wtforms.validators import DataRequired, Email, Length

# Define the registration form class, inheriting from FlaskForm
class RegistrationForm(FlaskForm):
    """
    User registration form.
    Allows users to register by providing their name, email, and password.
    """
    # Field for the user's name
    # The first argument is the label that will be displayed for this field.
    name = StringField('Name', 
                           validators=[
                               # Validator to ensure the field is not empty
                               DataRequired(message="Name is required."), 
                               # Validator to ensure the name has at least 3 characters
                               Length(min=3, message="Name must be at least 3 characters long.")
                           ])
    # Field for the user's email address
    email = StringField('Email Address',
                         validators=[
                             # Validator to ensure the field is not empty
                             DataRequired(message="Email is required."),
                             # Validator to ensure the email format is valid
                             Email(message="Please enter a valid email address.")
                         ])
    # Field for the user's password
    # PasswordField hides the characters as they are typed.
    password = PasswordField('Password', 
                               validators=[
                                   # Validator to ensure the field is not empty
                                   DataRequired(message="Password is required."),
                                   # Validator to ensure the password has at least 6 characters
                                   Length(min=6, message="Password must be at least 6 characters long.")
                               ])
    # Submit button for the form
    submit = SubmitField('Sign Up')
