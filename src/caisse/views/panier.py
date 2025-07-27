"""Vues pour la gestion du panier : ajout, retrait, affichage et finalisation de vente."""

from django.shortcuts import redirect, render
from django.contrib import messages

from caisse.models import Magasin

def ajouter_au_panier(request, magasin_id):
    """Ajoute un produit au panier pour un magasin donné."""
    if request.method == "POST":
        produit_id = int(request.POST["produit_id"])
        quantite = int(request.POST["quantite"])

        panier = request.session.get("panier", {})
        quantite_actuelle = panier.get(str(produit_id), 0)
        nouvelle_quantite = quantite_actuelle + quantite

        stock_dispo = stock_service.get_stock_entry(magasin_id, produit_id)
        if not stock_dispo or stock_dispo.quantite < nouvelle_quantite:
            messages.error(request, "Stock insuffisant.")
            return redirect("afficher_panier", magasin_id=magasin_id)

        panier[str(produit_id)] = nouvelle_quantite
        request.session["panier"] = panier
        messages.success(request, "Produit ajouté au panier.")

    return redirect("afficher_panier", magasin_id=magasin_id)


def retirer_du_panier(request, magasin_id, produit_id):
    """Retire un produit du panier."""
    panier = request.session.get("panier", {})
    if str(produit_id) in panier:
        del panier[str(produit_id)]
        request.session["panier"] = panier
        messages.success(request, "Produit retiré du panier.")
    else:
        messages.warning(request, "Produit non trouvé dans le panier.")
    return redirect("afficher_panier", magasin_id=magasin_id)


def afficher_panier_view(request, magasin_id):
    return render(request, "caisse/panier.html", {"magasin_id": magasin_id})

def finaliser_vente(request, magasin_id):
    """Finalise la vente en enregistrant les produits du panier."""
    panier = request.session.get("panier", {})
    if not panier:
        messages.warning(request, "Le panier est vide.")
        return redirect("afficher_panier", magasin_id=magasin_id)

    try:
        vente_service.creer_vente(panier, magasin_id)
        request.session["panier"] = {}
        messages.success(request, "Vente enregistrée avec succès.")
    except Exception as e:
        # Exception générique pour capturer toute erreur inattendue
        messages.error(request, f"Erreur lors de la vente : {e}")

    return redirect("afficher_panier", magasin_id=magasin_id)

