from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Carga un usuario desde su ID, necesario para el sistema de sesiones de Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Modelo de roles (Admin, Professor, Student, etc.)
class Role(db.Model):
    __tablename__ = 'role'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    # Relación inversa opcional (para ver usuarios asociados al rol)
    users = db.relationship('User', backref='role', lazy=True)

# Modelo de usuarios del sistema
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)  # Asegura suficiente espacio para el hash
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

    # Relación con encuestas creadas (si es creador)
    encuestas_creadas = db.relationship('Encuesta', backref='creador', lazy=True)

    def set_password(self, password: str):
        """
        Genera y guarda el hash de la contraseña.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Verifica si la contraseña ingresada es válida comparando con el hash.
        """
        return check_password_hash(self.password_hash, password)

# Modelo de Encuesta asociada a un creador
class Encuesta(db.Model):
    __tablename__ = 'encuesta'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_cierre = db.Column(db.DateTime, nullable=True)
    estado = db.Column(db.String(20), default='activo')
    creador_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relación con Preguntas (una encuesta tiene muchas preguntas)
    preguntas = db.relationship('Pregunta', backref='encuesta', lazy=True, cascade="all, delete-orphan")

# Modelo de Pregunta (asociada a una Encuesta)
class Pregunta(db.Model):
    __tablename__ = 'pregunta'
    id = db.Column(db.Integer, primary_key=True)
    texto_pregunta = db.Column(db.String(255), nullable=False)
    tipo_pregunta = db.Column(db.String(50), nullable=False)  # Ej: 'opcion_multiple', 'respuesta_abierta'
    encuesta_id = db.Column(db.Integer, db.ForeignKey('encuesta.id'), nullable=False)

    # Relación con Opciones (una pregunta de opción múltiple tiene varias opciones)
    opciones = db.relationship('Opcion', backref='pregunta', lazy=True, cascade="all, delete-orphan")

# Modelo de Opcion (asociada a una Pregunta de opción múltiple)
class Opcion(db.Model):
    __tablename__ = 'opcion'
    id = db.Column(db.Integer, primary_key=True)
    texto_opcion = db.Column(db.String(255), nullable=False)
    pregunta_id = db.Column(db.Integer, db.ForeignKey('pregunta.id'), nullable=False)

    # Relación con Votos (una opción puede tener muchos votos)
    votos = db.relationship('Voto', backref='opcion_elegida', lazy=True)

# Modelo de Voto (asociado a un Usuario y una Opción)
class Voto(db.Model):
    __tablename__ = 'voto'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    opcion_id = db.Column(db.Integer, db.ForeignKey('opcion.id'), nullable=False)
    encuesta_id = db.Column(db.Integer, db.ForeignKey('encuesta.id'), nullable=False) # Para facilitar consultas de votos por encuesta
    fecha_voto = db.Column(db.DateTime, default=datetime.utcnow)
    __table_args__ = (
        db.UniqueConstraint('user_id', 'opcion_id', name='uq_user_opcion_vote'),
    )
