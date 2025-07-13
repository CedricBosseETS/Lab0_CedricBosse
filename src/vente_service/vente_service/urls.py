"""
URL configuration for vente_service project.
"""
from django.contrib import admin
from django.urls import path
from vente_service.ventes.api_views import (
    ventes_par_magasin_api,
    finaliser_vente,
    annuler_vente
)

urlpatterns = [
    path('api/ventes/magasins/<int:magasin_id>/ventes/', ventes_par_magasin_api),
    path('api/ventes/rapports/', ventes_par_magasin_api, name='ventes_par_magasin'),
    path('api/ventes/panier/<int:magasin_id>/finaliser/', finaliser_vente, name='finaliser_vente'),
    path('api/ventes/panier/<int:magasin_id>/annuler/<int:vente_id>/', annuler_vente, name='annuler_vente'),
]
