from django.shortcuts import get_object_or_404
import requests
from caisse.models import Magasin

from django.test import TestCase

API_BASE_URL = "http://10.194.32.173:8000/api"


def get_all_magasins():
    """Retourne tous les magasins, quelle que soit leur catégorie."""
    return Magasin.objects.all()