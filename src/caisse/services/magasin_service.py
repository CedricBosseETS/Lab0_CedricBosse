from django.shortcuts import get_object_or_404
import requests
from caisse.models import Magasin

from django.test import TestCase

API_BASE_URL = "http://10.194.32.173:8000/api"


def get_all_magasins():
    """Retourne tous les magasins, quelle que soit leur catégorie."""
    return Magasin.objects.all()

def get_only_magasins():
    """Retourne uniquement les magasins de type 'magasin' depuis l'API."""
    try:
        response = requests.get(f"{API_BASE_URL}/magasins/")
        response.raise_for_status()
        all_magasins = response.json()
        return [m for m in all_magasins if m.get('type') == 'magasin']
    except requests.RequestException as e:
        print(f"Erreur lors de la récupération des magasins : {e}")
        return []

def get_magasin_by_id(magasin_id):
    """Retourne un magasin par son ID ou 404 s'il n'existe pas."""
    return get_object_or_404(Magasin, id=magasin_id)

def get_centre_logistique():
    """Retourne le magasin de type 'logistique' (centre logistique)."""
    return Magasin.objects.get(type='logistique')