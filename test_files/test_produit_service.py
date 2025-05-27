"""Fichier de test qui touche les produits"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from services.produit_service import afficher_produits, rechercher_produit, ajouter_produit
from unittest.mock import patch, MagicMock

@pytest.fixture(scope="function")
def session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_afficher_produits_aucun(capsys):
    with patch("services.produit_service.SessionLocal") as mock_session_local:
        mock_session = MagicMock()
        mock_session.query().all.return_value = []
        mock_session_local.return_value = mock_session

        afficher_produits()

        captured = capsys.readouterr()
        assert "Aucun produit trouvé." in captured.out

def test_rechercher_produit(capsys):
    with patch("builtins.input", side_effect=["eau", "1.5", "10"]):
        ajouter_produit()

    with patch("builtins.input", return_value="eau"):
        rechercher_produit()

    captured = capsys.readouterr()
    assert "eau" in captured.out
