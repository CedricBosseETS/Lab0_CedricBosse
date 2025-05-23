import os
from sqlalchemy import create_engine
from models.base import Base

# Récupération des variables d'environnement
db_user = os.getenv("DB_USER", "storeUser")
db_password = os.getenv("DB_PASSWORD", "storePassword")
db_host = os.getenv("DB_HOST", "db")
db_name = os.getenv("DB_NAME", "store")
db_port = os.getenv("DB_PORT", "3306")  # optionnel, par défaut 3306

# Construction dynamique de la chaîne de connexion
connection_string = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(connection_string)

def init_db():
    print("Création des tables…")
    Base.metadata.create_all(bind=engine)
    print("Base de données initialisée.")
