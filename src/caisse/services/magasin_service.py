from django.shortcuts import get_object_or_404
from caisse.models import Magasin

from django.test import TestCase

class MagasinTest(TestCase):
    def test_truc(self):
        ...


def get_all_magasins():
    """Retourne tous les magasins, quelle que soit leur catégorie."""
    return Magasin.objects.all()

def get_only_magasins():
    """Retourne uniquement les magasins de type 'magasin'."""
    return Magasin.objects.filter(type='magasin')

def get_magasin_by_id(magasin_id):
    """Retourne un magasin par son ID ou 404 s'il n'existe pas."""
    return get_object_or_404(Magasin, id=magasin_id)

def get_centre_logistique():
    """Retourne le magasin de type 'logistique' (centre logistique)."""
    return Magasin.objects.get(type='logistique')
