from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", data=None, message=None)


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    return f"Usuario: {username}, Contraseña: {password}"


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            error = "User name required."
        else:
            message = f"User {username} registered!"
            return render_template("home.html", message=message)
        
    return render_template("index.html", error=error)

if __name__ == "__main__":
    app.run(debug=True)