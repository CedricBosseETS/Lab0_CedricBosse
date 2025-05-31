"""Représente le stock de chaque produit dans chaque magasin"""
from django.db import models
from .produit import Produit
from .magasin import Magasin

class Stock(models.Model):
    """Représente le stock d’un produit dans un magasin"""
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name="stocks")
    magasin = models.ForeignKey(Magasin, on_delete=models.CASCADE, related_name="stocks")
    quantite = models.IntegerField()

    def __str__(self):
        return f"{self.quantite} de {self.produit.nom} à {self.magasin.nom}"
