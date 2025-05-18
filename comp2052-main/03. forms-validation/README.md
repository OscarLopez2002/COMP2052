# Login Form App

Una aplicación web para Login, construida con **Flask**, **WTForms**, **Jinja2** y **Bootstrap 5**. Incluye una REST API integrada y una interfaz web responsiva que permite entrar y validar el login de un usuario.

Los controles de entrada de datos y las reglas de validación del **Username** y el **Password** se definen en el código del servidor **app.py** utilizando la librería **WTForms**.

![Register Form](image.png)

---

## 🚀 Tecnologías utilizadas

- [Flask](https://flask.palletsprojects.com/) – Is a lightweight WSGI web application framework.
- [Jinja2](https://jinja.palletsprojects.com/) – Is a fast, expressive, extensible templating engine for web pages allow writing code similar to Python syntax.
- [wtforms](https://jinja.palletsprojects.com/) – Flexible forms validation and rendering library for Python web development.
- [Bootstrap 5](https://getbootstrap.com/) – Framework CSS para diseño moderno y responsivo
- HTML5, CSS3, JavaScript (mínimo)

---

## 📁 Estructura del Proyecto

```plaintext
simple-form/
│
├── static/
│   └── css/
│       └── styles.css         # Estilos personalizados
│
├── templates/
│   ├── base.html              # Layout principal
│   ├── home.html              # Página que se presenta luego de validar la entrada del usuario.
│   └── index.html             # Página principal con formulario para login.
│
├── app.py                     # App principal con vistas y lógica de frontend
└── requirements.txt           # Dependencias del proyecto
```

## 🔧 Instalación del App

### Clona el repositorio:

```plaintext
git clone https://github.com/tu-usuario/comp2052.git
cd simple-form
```

### Instala las dependencias:

```plaintext
pip install -r requirements.txt
```

### Ejecuta la aplicación:

```plaintext
python app.py
```

Abre tu navegador y ve a http://localhost:5000

## 📡 Endpoints de la API

### GET /login

Presenta la página web que contiene el formulario para login. Los elementos de interacción (cajas de texto y botones) son definidos en el código de Back-end (app.py).

![Login Form](image.png)

### POST /login

Procesa os datos entrados a través del formulario de login.
