from django.db import models
from django.utils.timezone import now

class Vente(models.Model):
    """Représente une vente."""
    date_heure = models.DateTimeField(default=now)
    total = models.FloatField()
    magasin_id = models.IntegerField()

    def __str__(self) -> str:
        vente_id = str(self.id) if self.id is not None else "non sauvegardée"
        return f"Vente {vente_id} - {self.total}$ (Magasin {self.magasinId})"

class VenteProduit(models.Model):
    """Représente les produits d'une vente."""
    vente_id = models.IntegerField() 
    produit_id = models.IntegerField()
    quantite = models.IntegerField()
    prix_unitaire = models.FloatField()

    def __str__(self) -> str:
        return f"{self.quantite} x Produit {self.produitId} dans vente {self.vente_id}"
