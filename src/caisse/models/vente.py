"""Représente les ventes dans la DB"""
from django.db import models
from django.utils.timezone import now
from .magasin import Magasin

class Vente(models.Model):
    """Représente une vente"""
    date_heure = models.DateTimeField(default=now)
    total = models.FloatField()
    magasin = models.ForeignKey(Magasin, on_delete=models.CASCADE, related_name="ventes")

    def __str__(self):
        return f"Vente {self.id} - {self.total}€"
