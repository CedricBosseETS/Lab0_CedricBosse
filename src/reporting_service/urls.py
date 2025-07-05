"""
Définit toutes les routes du micro service de rapports
"""
from django.urls import path, include, re_path
from .api_views import (
    rapport_ventes_api,
    tableau_de_bord_api,
    donnees_approvisionnement
)

urlpatterns = [
    path('api/maison_mere/<int:magasin_id>/rapport_ventes/', rapport_ventes_api, name='rapport_ventes_api'),
    path('api/maison_mere/<int:magasin_id>/tableau_de_bord/', tableau_de_bord_api, name='tableau_de_bord'),
    path('api/maison_mere/<int:magasin_id>/donnees_approvisionnement/', donnees_approvisionnement, name='donnees_approvisionnement'),
]