"""Ce module sert à la création de la base de donnée MySQL et à la gestion des sessions pour les usagers multiple"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from models.produit import Produit

# Connexion à la base de données via les variables d'environnement
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "3306")

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Comme indiqué plus haut, cette fonction instancie ma DB et insère des valleurs de départ"""
    print("Création des tables…")
    Base.metadata.create_all(bind=engine)

    # Ajout de produits si la table est vide
    session = SessionLocal()
    try:
        count = session.query(Produit).count()
        if count == 0:
            produits = [
                Produit(nom="Bouteille d'eau", prix=1.00, quantite_stock=50),
                Produit(nom="Sandwich", prix=4.50, quantite_stock=20),
                Produit(nom="Barre de chocolat", prix=1.80, quantite_stock=35),
                Produit(nom="Canette de coke", prix=2.00, quantite_stock=40),
            ]
            session.add_all(produits)
            session.commit()
    except Exception as e:
        session.rollback()
        print("Erreur lors de l’ajout des produits :", e)
    finally:
        session.close()

    print("Base de données initialisée.")
