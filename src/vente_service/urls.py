"""
Définit toutes les routes du micro service de rapports
"""
from django.urls import path, include, re_path
from .api_views import (
    ventes_par_magasin_api,
    finaliser_vente,
    annuler_vente
)

urlpatterns = [
    path("/magasins/<int:magasin_id>/ventes/", ventes_par_magasin_api),
    path('/rapports/ventes/', ventes_par_magasin_api, name='ventes_par_magasin'),
    path('/magasins/<int:magasin_id>/panier/finaliser/', finaliser_vente, name='finaliser_vente'),#adjust url to match anuler_vente
    path('/panier/<int:magasin_id>/annuler/<int:vente_id>/', annuler_vente, name='annuler_vente'),
]