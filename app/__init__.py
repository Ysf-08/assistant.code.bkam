import os
from flask import Flask
from .model import db
from .routes import main

def create_app():
    app = Flask(__name__)
    # app.config.from_object('config.Config')
    # Définir le chemin complet du fichier site.db dans le répertoire principal
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = '12345'

    # Initialiser la base de données avec l'application Flask
    db.init_app(app)
    # migrate = Migrate(app, db)
    # Importer et enregistrer les routes

    app.register_blueprint(main)

    return app
