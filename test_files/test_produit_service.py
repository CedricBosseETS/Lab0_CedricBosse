"""Fichier de test qui touche les produits"""
from services.produit_service import ajouter_produit, lister_produits, rechercher_produit


def test_ajouter_et_lister_produit():
    """Ajouter un produit fictif"""
    ajouter_produit("Test Produit", 9.99, 10)

    produits = lister_produits()
    noms = [p.nom for p in produits]

    assert "Test Produit" in noms

def test_rechercher_produit():
    """Cherche un produit dans la DB (il doit exister)"""
    produit = rechercher_produit("Test Produit")
    assert produit is not None
    assert produit.nom == "Test Produit"

    produit_id = produit.id
    meme_produit = rechercher_produit(str(produit_id))
    assert meme_produit.id == produit_id
