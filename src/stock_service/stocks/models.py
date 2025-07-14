from django.db import models

class Stock(models.Model):
    """Représente le stock d’un produit dans un magasin (via IDs, découplé)."""
    produit_id = models.IntegerField()
    magasin_id = models.IntegerField()
    quantite = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.quantite} unités — Produit {self.produit_id} dans Magasin {self.magasin_id}"
