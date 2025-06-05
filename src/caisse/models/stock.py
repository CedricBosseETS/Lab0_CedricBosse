"""Représente le stock de chaque produit dans chaque magasin."""

from django.db import models
from .produit import Produit
from .magasin import Magasin

class Stock(models.Model):
    """Représente le stock d’un produit dans un magasin."""
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name="stocks")
    magasin = models.ForeignKey(Magasin, on_delete=models.CASCADE, related_name="stocks")
    quantite = models.IntegerField()

    def __str__(self) -> str:
        nom_produit = getattr(self.produit, "nom", "Produit inconnu")
        nom_magasin = getattr(self.magasin, "nom", "Magasin inconnu")
        return f"{self.quantite} de {nom_produit} depuis {nom_magasin}"
