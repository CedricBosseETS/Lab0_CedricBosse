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
    def __init__(self, id, prix, quantite_stock=10):
        self.id = id
        self.prix = prix
        self.quantite_stock = quantite_stock

def test_creer_vente_sans_db():
    produit1 = ProduitMock(id=1, prix=5.0, quantite_stock=5)
    produit2 = ProduitMock(id=2, prix=3.0, quantite_stock=10)

    panier = [(produit1, 2), (produit2, 3)]

    session_mock = MagicMock()

    session_mock.query().with_for_update().filter_by().one.side_effect = [produit1, produit2]

    session_mock.add.return_value = None
    session_mock.flush.return_value = None
    session_mock.commit.return_value = None
    session_mock.rollback.return_value = None
    session_mock.close.return_value = None

    total = creer_vente(panier, session_mock)

    assert total == (5.0 * 2 + 3.0 * 3)
