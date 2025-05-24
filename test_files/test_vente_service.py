"""Fichier de test qui touche les ventes"""
from services.produit_service import ajouter_produit, rechercher_produit
from services.vente_service import creer_vente

def test_creer_vente():
    """Test qui fait une vente mais s'assure qu'il y a quelque chose dans la DB, ensuite vérifie la quantité"""
    ajouter_produit("Produit Vente", 5.00, 5)
    produit = rechercher_produit("Produit Vente")

    creer_vente([{"produit_id": produit.id, "quantite": 2}])

    produit_mis_a_jour = rechercher_produit(str(produit.id))
    assert produit_mis_a_jour.quantite == 3
