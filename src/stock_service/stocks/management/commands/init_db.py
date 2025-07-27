"""Commande Django pour initialiser la base de données avec les magasins, produits et stock de base."""
from django.core.management.base import BaseCommand
from stocks.models import Stock
import requests
import time

MAX_RETRIES = 10
RETRY_DELAY = 2  # secondes

def attendre_service(url):
    for i in range(MAX_RETRIES):
        try:
            response = requests.get(url, headers={"Host": "localhost"})
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"⏳ Tentative {i+1}/{MAX_RETRIES} : {url} non disponible ({e})")
            time.sleep(RETRY_DELAY)
    raise Exception(f"❌ Échec après {MAX_RETRIES} tentatives pour joindre {url}")

class Command(BaseCommand):
    help = "Initialise le stock de base dans le centre logistique."
    print("Initialisation du stock de base dans le centre logistique.")

    def handle(self, *args, **kwargs):
        if Stock.objects.exists():
            self.stdout.write("Stock déjà présent.")
            return

        try:
            produits = attendre_service("http://produit_service:5000/api/produits/")
            magasins = attendre_service("http://app:5000/api/magasins/")
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
