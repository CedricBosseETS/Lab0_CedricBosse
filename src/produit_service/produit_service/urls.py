"""
URL configuration for produit_service project.
"""
from django.contrib import admin
from django.urls import path
from produit_service.produits.api_views import (
    rechercher_produits_disponibles
)

urlpatterns = [
    path('api/produits/magasins/<int:magasin_id>/produits_disponibles/', rechercher_produits_disponibles, name='produits_disponibles')
]
