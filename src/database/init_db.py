"""Ce module sert à la création de la base de donnée MySQL
 et à la gestion des sessions pour les usagers multiples"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from models.produit import Produit

# Récupère les variables d'environnement
DB_USER = os.getenv("DB_USER", "caisse_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "supersecret")
DB_NAME = os.getenv("DB_NAME", "caisse_db")
DB_PORT = os.getenv("DB_PORT", "3306")

# Utilise "localhost" dans GitHub Actions, sinon "db" par défaut
if os.getenv("GITHUB_ACTIONS") == "true":
    DB_HOST = "127.0.0.1"
else:
    DB_HOST = os.getenv("DB_HOST", "db")

# URL complète
DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Création de l'engine SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Instancie la base de données sans insérer de données par défaut"""
    print("Création des tables…")
    Base.metadata.create_all(bind=engine)
    print("Base de données initialisée.")
