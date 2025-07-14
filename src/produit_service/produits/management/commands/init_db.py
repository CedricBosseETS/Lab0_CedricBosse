"""Commande Django pour initialiser la base de données avec les magasins, produits et stock de base."""
from django.core.management.base import BaseCommand
from produit_service.produits.models import Produit


class Command(BaseCommand):
    help = "Initialise les produits de base."

    def handle(self, *args, **kwargs):
        if Produit.objects.exists():
            self.stdout.write("Produits déjà présents.")
            return

        produits = [
            Produit(nom="Pommes", prix=1.50, description="Des pommes fraîches et croquantes."),
            Produit(nom="Bananes", prix=2.00, description="Des bananes mûres et sucrées."),
            Produit(nom="Lait", prix=2.50, description="Lait entier de qualité supérieure."),
            Produit(nom="Pain", prix=3.00, description="Pain artisanal fraîchement cuit."),
            Produit(nom="Eau", prix=1.00, description="Bouteille d'eau minérale naturelle."),
        ]

        Produit.objects.bulk_create(produits)
        self.stdout.write(self.style.SUCCESS("Produits de base créés."))

