"""
URL configuration for reporting_service project.
"""
from django.contrib import admin
from django.urls import path
from reporting.api_views import (
    rapport_ventes_api,
    tableau_de_bord_api,
    donnees_approvisionnement
)

urlpatterns = [
    path('api/reporting/<int:magasin_id>/rapport_ventes/', rapport_ventes_api, name='rapport_ventes_api'),
    path('api/reporting/<int:magasin_id>/tableau_de_bord/', tableau_de_bord_api, name='tableau_de_bord'),
    path('api/reporting/<int:magasin_id>/donnees_approvisionnement/', donnees_approvisionnement, name='donnees_approvisionnement'),
]
