# 🛡️ Mini Proyecto con Flask-Login

Este mini proyecto demuestra cómo implementar un sistema básico de autenticación de usuarios utilizando la extensión `Flask-Login` en Flask. Incluye inicio de sesión, manejo de sesiones, rutas protegidas y cierre de sesión.

## 📌 Características Principales

- Inicio de sesión de usuarios con verificación de credenciales.
- Mantenimiento de sesiones usando `Flask-Login`.
- Protección de rutas usando `@login_required`.
- Cierre de sesión y redirección automática.
- Plantillas HTML simples para login e inicio.

## 📁 Estructura del Proyecto

```
mini_login_project/
│
├── app.py                  # Lógica principal de la aplicación
├── requirements.txt        # Dependencias del proyecto
└── templates/
    ├── login.html          # Página de inicio de sesión
    └── home.html           # Página protegida tras autenticación
```

## ⚙️ Instalación y Ejecución

1. **Clonar o descargar el proyecto:**

```bash
git clone https://github.com/tu_usuario/comp2052.git
cd mini_login_project
```

2. **Crear y activar un entorno virtual:**

```bash
python -m venv venv
# En macOS/Linux:
source venv/bin/activate
# En Windows:
venv\Scripts\activate
```

3. **Instalar las dependencias:**

```bash
pip install -r requirements.txt
```

4. **Ejecutar la aplicación:**

```bash
python app.py
```

5. **Abrir el navegador en:**

```
http://127.0.0.1:5000/login
```

## 🔐 Usuarios Disponibles (Base simulada)

| Usuario | Contraseña |
| ------- | ---------- |
| admin   | 12345      |
| johndoe | secreto    |

## 🛠 Tecnologías Utilizadas

- **Python 3.8+**
- **Flask 2.x**
- **Flask-Login**

## 📚 Recursos Útiles

- [Documentación oficial de Flask](https://flask.palletsprojects.com/)
- [Flask-Login](https://flask-login.readthedocs.io/)

## 🚀 Posibles Extensiones

- Integración con base de datos real (SQLite, PostgreSQL, etc.).
- Registro de nuevos usuarios.
- Cifrado de contraseñas con `werkzeug.security`.
- Implementación de roles y permisos.
