from django.shortcuts import render, redirect, get_object_or_404
from services import magasin_service, stock_service
from caisse.models import Produit, Magasin
from django.contrib import messages

def page_caisse(request, magasin_id):
    magasin = magasin_service.get_magasin_by_id(magasin_id)
    
    action = request.GET.get("action")
    afficher_produits = (action == "afficher_produits")
    
    stocks = stock_service.get_stock_par_magasin(magasin_id) if afficher_produits else []

    context = {
        "magasin": magasin,
        "afficher_produits": afficher_produits,
        "stocks": stocks,
    }

    return render(request, "caisse.html", context)

def reapprovisionnement_view(request, magasin_id):
    magasin = magasin_service.get_magasin_by_id(magasin_id)
    centre_logistique = magasin_service.get_centre_logistique()

    stock_centre, stock_local = stock_service.get_stock_indexed_by_produit(centre_logistique.id, magasin.id)

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
            else:
                messages.error(request, msg)
        except ValueError as e:
            messages.error(request, str(e))

    context = {
        "magasin": magasin,
        "stock_centre": stock_centre,
        "stock_local": stock_local,
    }
    return render(request, "caisse/reapprovisionner.html", context)

def panier_view(request, magasin_id):
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

