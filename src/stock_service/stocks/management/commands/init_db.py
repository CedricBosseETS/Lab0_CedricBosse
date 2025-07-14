"""Commande Django pour initialiser la base de données avec les magasins, produits et stock de base."""
from django.core.management.base import BaseCommand
from stock_service.models import Stock
import requests


class Command(BaseCommand):
    help = "Initialise le stock de base dans le centre logistique."

    def handle(self, *args, **kwargs):
        if Stock.objects.exists():
            self.stdout.write("Stock déjà présent.")
            return

        try:
            produits = requests.get("http://produit_service:5000/api/produits/").json()
            magasins = requests.get("http://caisse:5000/api/magasins/").json()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erreur lors des appels API : {e}"))
            return

        centre_logistique = next((m for m in magasins if m["type"] == "logistique"), None)
        if not centre_logistique:
            self.stdout.write(self.style.ERROR("Centre logistique non trouvé"))
            return

        centre_id = centre_logistique["id"]
        stocks = [
            Stock(produit_id=produit["id"], magasin_id=centre_id, quantite=10000)
            for produit in produits
        ]

        Stock.objects.bulk_create(stocks)
        self.stdout.write(self.style.SUCCESS("Stock initial ajouté au centre logistique."))


