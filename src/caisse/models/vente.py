"""Représente les ventes dans la DB."""

from django.db import models
from django.utils.timezone import now
from .magasin import Magasin

class Vente(models.Model):
    """Représente une vente."""
    date_heure = models.DateTimeField(default=now)
    total = models.FloatField()
    magasin = models.ForeignKey(Magasin, on_delete=models.CASCADE, related_name="ventes")

    def __str__(self) -> str:
        # Accès sécurisé à l'id, au cas où l'objet n'aurait pas d'id (ex. non sauvegardé)
        vente_id = str(self.id) if self.id is not None else "non sauvegardée"
        return f"Vente {vente_id} - {self.total}$"
