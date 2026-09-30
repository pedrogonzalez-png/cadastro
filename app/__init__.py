from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os

db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    # Configuração do banco SQLite
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Chave usada pelo JWT
    app.config["JWT_SECRET_KEY"] = os.getenv(
        "JWT_SECRET_KEY",
        "chave-secreta-do-projeto-123456"
    )

    # Inicializa o banco e o JWT
    db.init_app(app)
    jwt.init_app(app)

    # Importa as rotas
    from app.routes.users import users_bp
    from app.routes.formularios import formularios_bp

    # Registra as rotas
    app.register_blueprint(users_bp)
    app.register_blueprint(formularios_bp)

    # Cria as tabelas do banco
    with app.app_context():
        db.create_all()

    return app