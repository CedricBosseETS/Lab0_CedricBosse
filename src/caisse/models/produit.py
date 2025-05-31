"""Représente les produits dans la DB"""
from django.db import models

class Produit(models.Model):
    """Représente un produit"""
    nom = models.CharField(max_length=100)
    prix = models.FloatField()

    def __str__(self):
        return self.nom
