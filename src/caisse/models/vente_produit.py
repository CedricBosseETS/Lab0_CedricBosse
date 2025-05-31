"""Représente les produits achetés dans une vente"""
from django.db import models
from .vente import Vente
from .produit import Produit

class VenteProduit(models.Model):
    """Représente les produits d'une vente"""
    vente = models.ForeignKey(Vente, on_delete=models.CASCADE, related_name="produits")
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.IntegerField()
    prix_unitaire = models.FloatField()

    def __str__(self):
        return f"{self.quantite} x {self.produit.nom} dans vente {self.vente.id}"
