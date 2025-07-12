"""Vues liées à la caisse : page caisse, recherche, réapprovisionnement, et affichage du panier."""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .services import magasin_service, produit_service
from stock_service.services import stock_service
from produit_service.services import produit_service
from caisse.models import Magasin
from produit_service.models import Produit


def page_caisse(request, magasin_id):
    """Affiche la page HTML de la caisse avec les produits disponibles du centre logistique pour réapprovisionnement."""
    magasin = magasin_service.get_magasin_by_id(magasin_id)
    centre_logistique = magasin_service.get_centre_logistique()
    produits_centre = stock_service.get_produits_disponibles(centre_logistique.id)
    stock_centre, _ = stock_service.get_stock_indexed_by_produit(
        centre_logistique.id, magasin.id
    )

    return render(request, "caisse.html", {
        "magasin_id": magasin_id,
        "magasin": magasin,
        "produits_centre": produits_centre,
        "stock_centre": stock_centre,
    })

def rechercher_produit(request, magasin_id):
    """Recherche un produit par son nom ou son identifiant dans un magasin."""
    query = request.GET.get("q", "").strip()
    produits_recherches = []

    if query:
        produits_recherches = produit_service.rechercher_produits_par_nom_ou_id(query)

    return render(request, "caisse.html", {
        "magasin": magasin_service.get_magasin_by_id(magasin_id),
        "magasin_id": magasin_id,
        "produits_recherches": produits_recherches,
    })


def reapprovisionnement_view(request, magasin_id):
    """Permet de transférer du stock depuis le centre logistique vers le magasin donné."""
    magasin = magasin_service.get_magasin_by_id(magasin_id)
    centre_logistique = magasin_service.get_centre_logistique()

    stock_centre, stock_local = stock_service.get_stock_indexed_by_produit(
        centre_logistique.id, magasin.id
    )

    if request.method == "POST":
        produit_id = int(request.POST["produit_id"])
        quantite = int(request.POST["quantite"])

        try:
            success, msg = stock_service.transferer_stock(
                produit_id,
                quantite,
                centre_logistique.id,
                magasin.id
            )
            if success:
                messages.success(request, msg)
                return redirect("reapprovisionner", magasin_id=magasin.id)
            messages.error(request, msg)
        except ValueError as error:
            messages.error(request, str(error))

    context = {
        "magasin": magasin,
        "stock_centre": stock_centre,
        "stock_local": stock_local,
    }
    return render(request, "caisse/reapprovisionner.html", context)


def panier_view(request, magasin_id):
    """Affiche les produits actuellement dans le panier pour le magasin."""
    magasin = get_object_or_404(Magasin, id=magasin_id)
    if "panier" not in request.session:
        request.session["panier"] = {}

    panier = request.session["panier"]
    produits = Produit.objects.filter(stock__magasin_id=magasin_id).select_related("stock")
    lignes = []

    for produit in produits:
        pid_str = str(produit.id)
        if pid_str in panier:
            lignes.append({
                "produit": produit,
                "quantite": panier[pid_str],
            })

    context = {
        "magasin": magasin,
        "produits": produits,
        "lignes": lignes,
    }
    return render(request, "caisse/panier.html", context)
