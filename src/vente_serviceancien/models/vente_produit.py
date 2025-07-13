"""Représente les produits achetés dans une vente."""

from django.db import models
from .vente import Vente
from produit_service.models import Produit

class VenteProduit(models.Model):
    """Représente les produits d'une vente."""
    vente = models.ForeignKey(Vente, on_delete=models.CASCADE, related_name="produits")
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.IntegerField()
    prix_unitaire = models.FloatField()

    def __str__(self) -> str:
        # Utiliser str() pour éviter les erreurs si produit ou vente est None (ex: en cours de suppression)
        produit_nom = str(self.produit.nom) if self.produit else "Produit inconnu"
        vente_id = str(self.vente.id) if self.vente else "Vente inconnue"
        return f"{self.quantite} x {produit_nom} dans vente {vente_id}"
