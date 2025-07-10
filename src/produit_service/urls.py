"""
Définit toutes les routes du micro service de rapports
"""
from django.urls import path, include, re_path
from .api_views import (
    rechercher_produits_disponibles
)

urlpatterns = [
    path('api/magasins/<int:magasin_id>/produits_disponibles/', rechercher_produits_disponibles, name='produits_disponibles')
]