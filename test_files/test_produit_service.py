"""Fichier de test qui touche les produits"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from services.produit_service import ajouter_produit, afficher_produits, rechercher_produit
from unittest.mock import patch
from database.init_db import SessionLocal
from src.models.produit import Produit
from src.produit_service import rechercher_produit

@pytest.fixture(scope="function")
def session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_ajouter_et_afficher_produit(capsys):
    session = SessionLocal()
    try:
        ajouter_produit("Test Produit", 9.99, 10)

        afficher_produits()
        captured = capsys.readouterr()

        assert "Test Produit" in captured.out
        assert "9.99$" in captured.out
    finally:
        session.rollback()
        session.close()

def test_rechercher_produit(capsys):

    # Simuler l'entrée utilisateur avec patch uniquement dans le test
    with patch("builtins.input", return_value="eau"):
        rechercher_produit()

    # Capture la sortie console
    captured = capsys.readouterr()
    assert "eau" in captured.out
