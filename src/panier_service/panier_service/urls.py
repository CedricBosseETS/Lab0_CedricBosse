"""
URL configuration for panier_service project.
"""
from django.contrib import admin
from django.urls import path
from panier_service.panier.api_views import (
    afficher_panier,
    ajouter_au_panier,
    retirer_du_panier,
    vider_panier
)

urlpatterns = [
    path("api/panier/magasins/<int:magasin_id>/panier/", afficher_panier),
    path("api/panier/magasins/<int:magasin_id>/panier/ajouter/", ajouter_au_panier),
    path("api/panier/magasins/<int:magasin_id>/panier/retirer/", retirer_du_panier),
    path("api/panier/magasins/<int:magasin_id>/panier/vider/", vider_panier) 
]
