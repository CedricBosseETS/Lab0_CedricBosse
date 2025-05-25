"""Fichier de test qui touche les ventes"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.init_db import SessionLocal
from models.base import Base
from services.produit_service import ajouter_produit, rechercher_produit
from services.vente_service import creer_vente

@pytest.fixture(scope="function")
def session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_creer_vente():
    # Étape 1 : Ajouter un produit de test
    ajouter_produit("Produit Vente", 5.00, 5)

    # Étape 2 : Aller chercher le produit depuis la DB directement (pas avec input())
    session = SessionLocal()
    try:
        produit = session.query(Produit).filter_by(nom="Produit Vente").first()
        assert produit is not None

        # Étape 3 : Créer un panier et faire la vente
        panier = [(produit, 2)]
        creer_vente(panier)
    finally:
        session.close()

    # Étape 4 : Vérifier que le stock est bien diminué
    session = SessionLocal()
    try:
        produit_mis_a_jour = session.query(Produit).filter_by(nom="Produit Vente").first()
        assert produit_mis_a_jour.quantite_stock == 3
    finally:
        session.close()
