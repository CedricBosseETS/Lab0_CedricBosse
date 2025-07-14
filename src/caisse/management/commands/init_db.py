"""Commande Django pour initialiser la base de données avec les magasins, produits et stock de base."""
from django.core.management.base import BaseCommand
from caisse.models import Magasin
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Initialise les magasins de base et crée un superutilisateur."

    def handle(self, *args, **kwargs):
        # Création du super utilisateur
        if not User.objects.filter(username="super_caisse_user").exists():
            User.objects.create_superuser(
                username="super_caisse_user",
                email="admin@example.com",
                password="supersecret"
            )
            self.stdout.write(self.style.SUCCESS("Super utilisateur 'super_caisse_user' créé."))
        else:
            self.stdout.write("Super utilisateur déjà présent.")

        # Création des magasins
        if Magasin.objects.exists():
            self.stdout.write("Magasins déjà présents.")
            return

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

