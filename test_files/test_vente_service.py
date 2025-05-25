"""Fichier de test qui touche les ventes"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from services.vente_service import creer_vente
from unittest.mock import MagicMock

@pytest.fixture(scope="function")
def session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

class ProduitMock:
    def __init__(self, id, prix):
        self.id = id
        self.prix = prix
        self.quantite_stock = 10

def test_creer_vente_sans_db():
    # Prépare un panier fictif
    produit1 = ProduitMock(id=1, prix=5.0)
    produit2 = ProduitMock(id=2, prix=3.0)

    panier = [(produit1, 2), (produit2, 3)]

    # Mock de la session avec méthode add, flush, commit, rollback
    session_mock = MagicMock()
    session_mock.add.return_value = None
    session_mock.flush.return_value = None
    session_mock.commit.return_value = None
    session_mock.rollback.return_value = None
    session_mock.close.return_value = None

    # Appelle la fonction avec le panier et la session mockée
    total = creer_vente(panier, session_mock)

    # Vérifie le total calculé
    assert total == (2 * 5.0 + 3 * 3.0)

    # Vérifie que add a été appelé plusieurs fois (vente + lignes)
    assert session_mock.add.call_count >= 3

    # Vérifie que flush, commit et close ont été appelés
    session_mock.flush.assert_called_once()
    session_mock.commit.assert_called_once()
    session_mock.close.assert_called_once()

    # Vérifie que les stocks ont bien été décrémentés
    assert produit1.quantite_stock == 8
    assert produit2.quantite_stock == 7
