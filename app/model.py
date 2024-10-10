from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Initialiser l'instance SQLAlchemy pour gérer la base de données
db = SQLAlchemy()

# Définir le modèle User qui représente la table des utilisateurs dans la base de données
class User(db.Model):
    # Définir les colonnes de la table User
    id = db.Column(db.Integer, primary_key=True)  # Identifiant unique pour chaque utilisateur
    username = db.Column(db.String(150), unique=True, nullable=False)  # Nom d'utilisateur unique
    email = db.Column(db.String(150), unique=True, nullable=False)  # Adresse email unique
    password_hash = db.Column(db.String(128), nullable=False)  # Hash du mot de passe de l'utilisateur

    # Méthode pour définir le mot de passe en le hachant
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Méthode pour vérifier si le mot de passe fourni correspond au hash stocké
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
