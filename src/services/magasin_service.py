from django.shortcuts import get_object_or_404
from caisse.models import Magasin

def get_all_magasins():
    return Magasin.objects.all()

def get_only_magasins():
    return Magasin.objects.filter(type='magasin')

def get_magasin_by_id(magasin_id):
    return get_object_or_404(Magasin, id=magasin_id)

def get_centre_logistique():
    return Magasin.objects.get(type="logistique")
