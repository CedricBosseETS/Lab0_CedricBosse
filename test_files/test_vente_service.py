"""Fichier de test qui touche les ventes"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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

def test_creer_vente(session):
    """Test qui fait une vente, vérifie que la quantité est réduite"""
    ajouter_produit("Produit Vente", 5.00, 5, session)
    produit = rechercher_produit(session, "Produit Vente")

    creer_vente([{"produit_id": produit.id, "quantite": 2}], session)

    produit_mis_a_jour = rechercher_produit(session, str(produit.id))
    assert produit_mis_a_jour.quantite_stock == 3
