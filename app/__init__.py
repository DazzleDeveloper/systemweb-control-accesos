from flask import Flask
from app.routes.main import main
from app.routes.registro import registro  # 👈 AÑADIR
from app.routes.login import login
from app.routes.login import login





def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'clave-segura'

    # Importar y registrar blueprints
    from .routes.main import main
    app.register_blueprint(main)
    app.register_blueprint(registro)  # 👈 AÑADIR
    app.register_blueprint(login)
    return app
