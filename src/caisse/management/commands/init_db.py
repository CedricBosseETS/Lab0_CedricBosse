from django.core.management.base import BaseCommand
from caisse.models import Magasin, Produit, Stock

class Command(BaseCommand):
    help = "Initialise la base de données avec les magasins et le stock de base."

    def handle(self, *args, **options):
        self.stdout.write("Initialisation de la base de données avec Django ORM...")

        # Création des magasins si nécessaires
        if Magasin.objects.count() == 0:
            magasins = [
                Magasin(nom="Magasin un", quartier="un", type="magasin"),
                Magasin(nom="Magasin deux", quartier="deux", type="magasin"),
                Magasin(nom="Magasin trois", quartier="trois", type="magasin"),
                Magasin(nom="Magasin quatre", quartier="quatre", type="magasin"),
                Magasin(nom="Magasin cinq", quartier="cinq", type="magasin"),
                Magasin(nom="Centre logistique", quartier="Centre logistique", type="logistique"),
                Magasin(nom="Maison mère", quartier="Administration", type="admin"),
            ]
            Magasin.objects.bulk_create(magasins)
            self.stdout.write(self.style.SUCCESS("Magasins de base créés."))
        else:
            self.stdout.write("Magasins déjà présents, rien à faire.")

        # Ajout de stock de base si aucun produit n'existe
        if Produit.objects.count() == 0:
            produits = [
                Produit(nom="Pommes", prix=1.50),
                Produit(nom="Bananes", prix=2.00),
                Produit(nom="Lait", prix=2.50),
                Produit(nom="Pain", prix=3.00),
                Produit(nom="Eau", prix=1.00),
            ]
            Produit.objects.bulk_create(produits)
            self.stdout.write(self.style.SUCCESS("Produits de base créés."))
        else:
            self.stdout.write("Produits déjà présents, rien à faire.")

        # Ajout de stock dans le centre logistique si vide
        if Stock.objects.count() == 0:
            centre_logistique = Magasin.objects.get(type="logistique")
            for produit in Produit.objects.all():
                Stock.objects.create(produit=produit, magasin=centre_logistique, quantite=100)
            self.stdout.write(self.style.SUCCESS("Stock de base ajouté au centre logistique."))
        else:
            self.stdout.write("Stock déjà présent, rien à faire.")

        self.stdout.write(self.style.SUCCESS("Base de données initialisée."))
