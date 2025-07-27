"""
URL configuration for stock_service project.
"""
from django.contrib import admin
from django.urls import path
from stocks.api_views import (
    reapprovisionner_api,
    transferer_stock,
    bulk_reapprovisionner_api,
    produits_disponibles_api,
    stock_indexe_api
)

urlpatterns = [
    path('api/stock/magasins/<int:magasin_id>/reapprovisionner/', reapprovisionner_api, name='reapprovisionner_api'),
    path('api/stock/transferer/', transferer_stock, name='transferer_stock'),
    path('api/stock/centre/<int:magasin_id>/bulk_reapprovisionner/', bulk_reapprovisionner_api), 
    path('api/stock/produits_disponibles/<int:magasin_id>/', produits_disponibles_api),
    path('api/stock/stock_indexe/<int:centre_id>/<int:magasin_id>/', stock_indexe_api),
]
