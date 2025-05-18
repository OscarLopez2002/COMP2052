import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

def create_app():
    # Define template and static directories
    curr_dir = os.path.abspath(os.path.dirname(__file__))
    template_dir = os.path.join(curr_dir, '..', 'templates')
    static_dir = os.path.join(curr_dir, '..', 'static')

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    # Load configuration
    app.config.from_object('config.Config')

    # Register routes
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
