"""Vues liées à la caisse : page caisse, recherche, réapprovisionnement, et affichage du panier."""
from rest_framework.response import Response
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from django.http import HttpResponseNotFound, HttpResponseServerError
import requests

from caisse.services import magasin_service
#from stock_service.stocks.services import stock_service
#from produit_service.produits.services import produit_service
from caisse.models import Magasin
#from produit_service.produits.models import Produit


def page_caisse(request, magasin_id):
    """Affiche la page HTML de la caisse avec les produits disponibles du centre logistique pour réapprovisionnement."""

    headers = {}
    if request.user.is_authenticated and request.session.session_key:
        session_cookie = request.COOKIES.get('sessionid')
        if session_cookie:
            headers['Cookie'] = f'sessionid={session_cookie}'

    # 1. Récupération du magasin
    magasin = magasin_service.get_magasin_by_id(magasin_id)

    # 2. Récupération du centre logistique
    centre_logistique = magasin_service.get_centre_logistique()

    # 3. Produits disponibles au centre logistique
    try:
        resp_produits = requests.get(f"http://localhost:5000/api/stock/produits_disponibles/{magasin.id}/", headers=headers)
        resp_produits.raise_for_status()
        produits_centre = resp_produits.json()
    except requests.exceptions.RequestException as e:
        return HttpResponseServerError(f"Erreur lors de la récupération des produits du centre : {str(e)}")

    # 4. Stock indexé
    try:
        resp_stock = requests.get(f"http://localhost:5000/api/stock/stock_indexe/{centre_logistique.id}/{magasin.id}/", headers=headers)
        resp_stock.raise_for_status()
        stock_data = resp_stock.json()
        stock_centre = stock_data.get("stock_centre", {})
    except requests.exceptions.RequestException as e:
        return HttpResponseServerError(f"Erreur lors de la récupération du stock : {str(e)}")

    # 5. Affichage de la page caisse
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
