from django.db import models
from enum import Enum

class EtatCommande(Enum):
    EN_ATTENTE = "en_attente"
    STOCK_RESERVE = "stock_reserve"
    PAYE = "paye"
    CONFIRMEE = "confirmee"
    ANNULEE = "annulee"

class Commande(models.Model):
    id_commande = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    etat = models.CharField(max_length=30, choices=[(tag.name, tag.value) for tag in EtatCommande])
    date_creation = models.DateTimeField(auto_now_add=True)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
