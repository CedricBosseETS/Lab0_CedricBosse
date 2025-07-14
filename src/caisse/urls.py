"""
Définit toutes les routes de l'application 'caisse' pour l'acceuil et la documentation
"""

from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import gestion, home, magasins, caisse, panier, vente #will have to change/split them in services
from .views.panier import afficher_panier_view #same here
from caisse.api_views import get_magasin_by_id_api, get_centre_logistique_api


from caisse.api_views import MagasinViewSet

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
    path('api/magasins/<int:id>/', get_magasin_by_id),
    path('api/magasins/centre_logistique/', get_centre_logistique),

    # --- Vues classiques (UI) ---
    path('', home.home_view, name='home'),
    path('magasins/', magasins.page_magasins, name='magasins'),
    path('caisse/<int:magasin_id>/', caisse.page_caisse, name='page_caisse'),
    path('panier/<int:magasin_id>/', afficher_panier_view, name='panier'), #panier.afficher panier

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
