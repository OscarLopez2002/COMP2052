import os

class Config:
    """
    Configuración general de la aplicación Flask.
    Puede extenderse a diferentes entornos (Desarrollo, Producción, etc.).
    """

    # Clave secreta para proteger sesiones y formularios (CSRF)
    # En producción, se recomienda definir esta variable en el entorno
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clave-secreta-flask')

    # URI de conexión a la base de datos
    # Configuración para XAMPP (el usuario root no tiene contraseña por defecto)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+pymysql://root:@localhost:3306/encuestas_votaciones'
    )
    
    # Puerto de MySQL (XAMPP usa el puerto 3306 por defecto)
    MYSQL_PORT = 3306

    # Desactiva el sistema de seguimiento de modificaciones de SQLAlchemy (mejora el rendimiento)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
