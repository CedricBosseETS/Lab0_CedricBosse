from django.urls import path
from .views import home, magasins, admin_page, caisse, panier, vente

urlpatterns = [
    path('', home.home_view, name='home'),
    path('magasins/', magasins.page_magasins, name='magasins'),
    path('admin_page/', admin_page.admin_view, name='admin_page'),
    path('caisse/<int:magasin_id>/', caisse.page_caisse, name='page_caisse'),
    path('reapprovisionner/<int:magasin_id>/', caisse.reapprovisionnement_view, name='reapprovisionner'),
    path('<int:magasin_id>/recherche/', caisse.rechercher_produit, name='rechercher_produit'),

    path("magasin/<int:magasin_id>/panier/", panier.afficher_panier, name="panier"),
    path("magasin/<int:magasin_id>/panier/", panier.afficher_panier, name="afficher_panier"),
    path('<int:magasin_id>/panier/ajouter/', panier.ajouter_au_panier, name='ajouter_panier'),
    path('<int:magasin_id>/panier/retirer/<int:produit_id>/', panier.retirer_du_panier, name='retirer_du_panier'),
    path('<int:magasin_id>/panier/finaliser/', panier.finaliser_vente, name='finaliser_panier'),

    path('<int:magasin_id>/ventes/', vente.liste_ventes, name='liste_ventes'),
    path('<int:magasin_id>/ventes/<int:vente_id>/annuler/', vente.annuler_vente, name='annuler_vente'),
]
