"""
URL configuration for produit_service project.
"""
from django.contrib import admin
from django.urls import path
from produits.api_views import (
    rechercher_produits_disponibles,
    get_produit,
    get_all_produits
)

urlpatterns = [
    path('api/produits/magasins/<int:magasin_id>/produits_disponibles/', rechercher_produits_disponibles, name='produits_disponibles'),
    path("api/produits/<int:pk>/", get_produit),
    path("api/produits/", get_all_produits),
]
