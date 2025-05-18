from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class RegistrationForm(FlaskForm):
    name = StringField('Nombre', validators=[
        DataRequired(message="El nombre es obligatorio."),
        Length(min=3, message="El nombre debe tener al menos 3 caracteres.")
    ])
    email = StringField('Correo', validators=[
        DataRequired(message="El correo es obligatorio."),
        Email(message="Formato de correo inválido.")
    ])
    password = PasswordField('Contraseña', validators=[
        DataRequired(message="La contraseña es obligatoria."),
        Length(min=6, message="La contraseña debe tener al menos 6 caracteres.")
    ])
    submit = SubmitField('Registrar')
