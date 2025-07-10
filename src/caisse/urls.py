"""
Définit toutes les routes de l'application 'caisse' :
accueil, gestion des magasins, caisse, panier, ventes et administration.
"""

from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import gestion, home, magasins, caisse, panier, vente
from .views.panier import afficher_panier_view

from .api_views import (
    MagasinViewSet,
    ProduitViewSet,
    StockViewSet,
    VenteViewSet,
    transferer_stock,
    afficher_panier,
    ajouter_au_panier,
    retirer_du_panier,
    vider_panier,
    finaliser_vente,
    annuler_vente,
    ventes_par_magasin_api,
    approvisionner,
    reapprovisionner_api,
    rechercher_produits_disponibles,
    bulk_reapprovisionner_api   
)

from reporting_service import urls as reporting_urls
from vente_service import urls as vente_urls

# Documentation Swagger/OpenAPI
schema_view = get_schema_view(
    openapi.Info(
        title="Caisse API",
        default_version='v1',
        description="Documentation de l'API de l'application de caisse",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Router DRF pour les viewsets
router = DefaultRouter()
router.register(r'magasins', MagasinViewSet, basename='magasin')
router.register(r'produits', ProduitViewSet, basename='produit')
router.register(r'stocks', StockViewSet, basename='stock')
router.register(r'ventes', VenteViewSet, basename='vente')

urlpatterns = [
    # Prometheus metrics (root include ajoutera /metrics/)
    path('', include('django_prometheus.urls')),

    # --- Documentation ---
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),

    # --- API REST ---
    path('api/', include(router.urls)),
    path('api/magasins/<int:magasin_id>/reapprovisionner/', reapprovisionner_api, name='reapprovisionner_api'),
    #path("api/magasins/<int:magasin_id>/ventes/", ventes_par_magasin_api), moved to vente_service
    #path('api/magasins/<int:magasin_id>/produits_disponibles/', rechercher_produits_disponibles, name='produits_disponibles'), dans produit_service
    path('api/stock/transferer/', transferer_stock, name='transferer_stock'),
    path("api/magasins/<int:magasin_id>/panier/", afficher_panier),
    path("api/magasins/<int:magasin_id>/panier/ajouter/", ajouter_au_panier),
    path("api/magasins/<int:magasin_id>/panier/retirer/", retirer_du_panier),
    path("api/magasins/<int:magasin_id>/panier/vider/", vider_panier),
    # les urls ont changer donc va falloir ajouter /vente devant les routes en utilisation
    path('api/vente/', include(vente_urls)),
    #path('api/magasins/<int:magasin_id>/panier/finaliser/', finaliser_vente, name='finaliser_vente'),#adjust url to match anuler_vente moved to vente_service
    #path('api/panier/<int:magasin_id>/annuler/<int:vente_id>/', annuler_vente, name='annuler_vente'), moved to vente_service
    #path('api/rapports/ventes/', ventes_par_magasin_api, name='ventes_par_magasin'), moved to vente_service
    path('api/maison_mere/', include(reporting_urls)), #pas sur de si c'est bien comme ça
    #path('api/maison_mere/<int:magasin_id>/rapport_ventes/', rapport_ventes_api, name='rapport_ventes_api'), déplacé dans reporting_service
    #path('api/maison_mere/<int:magasin_id>/tableau_de_bord/', tableau_de_bord_api, name='tableau_de_bord'), déplacé dans reporting_service
    #path('api/maison_mere/<int:magasin_id>/donnees_approvisionnement/', donnees_approvisionnement, name='donnees_approvisionnement'), déplacé dans reporting_service
    path('api/centre/<int:magasin_id>/bulk_reapprovisionner/', bulk_reapprovisionner_api), 
    #path('api/maison_mere/<int:magasin_id>/approvisionner/', approvisionner, name='approvisionner'), doit être réparer
    #path('api/maison_mere/<int:centre_id>/approvisionner/', approvisionner, name='approvisionner'),#Je pense n'est pas utilisé

    # --- Vues classiques (UI) ---
    path('', home.home_view, name='home'),
    path('magasins/', magasins.page_magasins, name='magasins'),
    path('caisse/<int:magasin_id>/', caisse.page_caisse, name='page_caisse'),
    path('panier/<int:magasin_id>/', afficher_panier_view, name='panier'),

    # Administration générale
    path('gestion/', gestion.admin_page, name='admin_page'),
    path('gestion/<int:magasin_id>/', gestion.admin_entite, name='admin_entite'),

    # Rapports & dashboard depuis l’administration
    path('gestion/<int:magasin_id>/rapport/', gestion.rapport_ventes, name='rapport_ventes'),
    path('gestion/<int:magasin_id>/dashboard/', gestion.tableau_de_bord, name='tableau_de_bord'),

    # Gestion des produits (maison_mere)
    path('gestion/<int:magasin_id>/produits/', gestion.modifier_produits_depuis_maison_mere,
         name='modifier_produits_depuis_maison_mere'),
    path('gestion/produits/<int:produit_id>/modifier/', gestion.modifier_produit, name='modifier_produit'),

    # Approvisionnement depuis le centre logistique
    path('centre/<int:centre_logistique_id>/approvisionner/', gestion.approvisionner_magasin,
         name='approvisionner_magasin'),
]
