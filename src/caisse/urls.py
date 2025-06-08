"""
Définit toutes les routes de l'application 'caisse' :
accueil, gestion des magasins, caisse, panier, ventes et administration.
"""

from .views import gestion, home, magasins, caisse, panier, vente
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import MagasinViewSet, ProduitViewSet, StockViewSet, VenteViewSet, reapprovisionner_api


router = DefaultRouter()
router.register(r'magasins', MagasinViewSet, basename='magasin')
router.register(r'stocks', StockViewSet, basename='stock')

urlpatterns = router.urls

urlpatterns = [
    # API REST
    path('api/', include(router.urls)),
    path('api/magasins/<int:magasin_id>/reapprovisionner/', reapprovisionner_api, name='reapprovisionner_api'),



    # Vues classiques ici
    path('', home.home_view, name='home'),
    path('magasins/', magasins.page_magasins, name='magasins'),
    path('caisse/<int:magasin_id>/', caisse.page_caisse, name='page_caisse'),
    path(
        'reapprovisionner/<int:magasin_id>/',
        caisse.reapprovisionnement_view,
        name='reapprovisionner'
    ),
    path(
        '<int:magasin_id>/recherche/',
        caisse.rechercher_produit,
        name='rechercher_produit'
    ),

    path("magasin/<int:magasin_id>/panier/", panier.afficher_panier, name="panier"),
    path(
        '<int:magasin_id>/panier/ajouter/',
        panier.ajouter_au_panier,
        name='ajouter_panier'
    ),
    path(
        '<int:magasin_id>/panier/retirer/<int:produit_id>/',
        panier.retirer_du_panier,
        name='retirer_du_panier'
    ),
    path(
        '<int:magasin_id>/panier/finaliser/',
        panier.finaliser_vente,
        name='finaliser_panier'
    ),

    path('<int:magasin_id>/ventes/', vente.liste_ventes, name='liste_ventes'),
    path(
        '<int:magasin_id>/ventes/<int:vente_id>/annuler/',
        vente.annuler_vente,
        name='annuler_vente'
    ),

    path("gestion/", gestion.admin_page, name="admin_page"),
    path(
        "gestion/<int:magasin_id>/",
        gestion.admin_entite,
        name="admin_entite"
    ),
    path(
        'gestion/<int:magasin_id>/rapport/',
        gestion.rapport_ventes,
        name='rapport_ventes'
    ),
    path(
        'gestion/<int:magasin_id>/dashboard/',
        gestion.tableau_de_bord,
        name='tableau_de_bord'
    ),
    path(
        'gestion/<int:magasin_id>/produits/',
        gestion.modifier_produits_depuis_maison_mere,
        name='modifier_produits_depuis_maison_mere'
    ),
    path(
        'gestion/produits/<int:produit_id>/modifier/',
        gestion.modifier_produit,
        name='modifier_produit'
    ),
    path(
        'centre/<int:centre_logistique_id>/approvisionner/',
        gestion.approvisionner_magasin,
        name='approvisionner_magasin'
    ),
]
