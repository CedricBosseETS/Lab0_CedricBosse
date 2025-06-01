from django.core.management.base import BaseCommand
from caisse.models import Magasin

class Command(BaseCommand):
    help = "Initialise la base de données en créant les magasins de base."

    def handle(self, *args, **options):
        self.stdout.write("Initialisation de la base de données avec Django ORM...")

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

        self.stdout.write("Base de données initialisée.")