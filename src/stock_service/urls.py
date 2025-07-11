"""
Définit toutes les routes du micro service de rapports
"""
from django.urls import path, include, re_path
from .api_views import (
    reapprovisionner_api,
    transferer_stock,
    bulk_reapprovisionner_api
)

urlpatterns = [
    path('magasins/<int:magasin_id>/reapprovisionner/', reapprovisionner_api, name='reapprovisionner_api'),
    path('stock/transferer/', transferer_stock, name='transferer_stock'),
    path('centre/<int:magasin_id>/bulk_reapprovisionner/', bulk_reapprovisionner_api), 
]