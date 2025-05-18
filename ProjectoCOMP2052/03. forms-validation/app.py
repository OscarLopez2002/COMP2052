from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)

app.config["SECRET_KEY"] = "mi_clave_secreta"

class LoginForm(FlaskForm):
    username = StringField("Username", # definir input box para el username
        validators=[DataRequired(), Length(min=3)],
        render_kw={"placeholder": "Your email"})
    
    password = PasswordField("Password", # definir input box para el password
        validators=[DataRequired()],
        render_kw={"placeholder": "Your password"})
    
    submit = SubmitField("Login",  # definir el botón de submit
        render_kw={"class": "btn btn-primary"}) # aplicar clases de CSS


@app.route("/", methods=["GET"])
def index():
    return login() # Llamar a la función login() en la dirección http://127.0.0.1:5000

@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm() # Definir las reglas de validación

    if form.validate_on_submit(): # Validar los datos entrados contra las reglas
        message = f"Usuario: {form.username.data}"
        return render_template("home.html", message=message)
    
    return render_template("index.html.jinja2", form=form)

if __name__ == "__main__":
    app.run(debug=True)
