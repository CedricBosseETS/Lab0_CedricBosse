"""
Définit toutes les routes du micro service de rapports
"""
from django.urls import path, include, re_path
from .api_views import (
    afficher_panier,
    ajouter_au_panier,
    retirer_du_panier,
    vider_panier
)

urlpatterns = [
    path("api/magasins/<int:magasin_id>/panier/", afficher_panier),
    path("api/magasins/<int:magasin_id>/panier/ajouter/", ajouter_au_panier),
    path("api/magasins/<int:magasin_id>/panier/retirer/", retirer_du_panier),
    path("api/magasins/<int:magasin_id>/panier/vider/", vider_panier) 
]