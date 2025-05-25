"""Fichier de test qui touche les produits"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from services.produit_service import ajouter_produit, afficher_produits, rechercher_produit

@pytest.fixture(scope="function")
def session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_ajouter_et_afficher_produit(session):
    """Ajouter un produit fictif"""
    ajouter_produit("Test Produit", 9.99, 10, session)

    produits = afficher_produits(session)
    noms = [p.nom for p in produits]

    assert "Test Produit" in noms

def test_rechercher_produit(session):
    """Cherche un produit dans la DB (il doit exister)"""
    produit = ajouter_produit("Test Produit", 9.99, 10, session)

    produit_retrouve = rechercher_produit(session, "Test Produit")
    assert produit_retrouve is not None
    assert produit_retrouve.nom == "Test Produit"

    produit_id = produit_retrouve.id
    meme_produit = rechercher_produit(session, str(produit_id))
    assert meme_produit.id == produit_id
