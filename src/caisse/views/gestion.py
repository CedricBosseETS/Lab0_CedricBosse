"""Vue de gestion administrative : maison mère, centre logistique, rapports, approvisionnement."""

from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from vente_service.services import vente_service
from produit_service.services import produit_service
from stock_service.services import stock_service
from reporting_service.services import reporting_service
from caisse.models import Magasin
from produit_service.models import Produit
from caisse.services import magasin_service

def admin_page(request):
    """Affiche les entités administratives (hors magasins)."""
    magasins = reporting_service.get_all_magasins()
    entites_admin = [m for m in magasins if m.type != 'magasin']
    return render(request, 'gestion.html', {'entites_admin': entites_admin})


def admin_entite(request, magasin_id):
    """Affiche l'interface appropriée selon le type d'entité."""
    magasin = magasin_service.get_magasin_by_id(magasin_id)
    if magasin.type == 'admin':
        return render(request, 'gestion/maison_mere.html', {'magasin': magasin})
    return render(request, 'gestion/centre_logistique.html', {'magasin': magasin})


def rapport_ventes(request, magasin_id):
    """Affiche un rapport des ventes et des stocks."""
    magasin = magasin_service.get_magasin_by_id(magasin_id)
    ventes_par_magasin = vente_service.get_ventes_par_magasin()
    produits_plus_vendus = vente_service.get_produits_les_plus_vendus()
    stocks_restant = stock_service.get_stock_total_par_magasin()

    context = {
        'magasin': magasin,
        'ventes_par_magasin': ventes_par_magasin,
        'produits_plus_vendus': produits_plus_vendus,
        'stocks_restant': stocks_restant
    }
    return render(request, 'gestion/rapport_ventes.html', context)


def tableau_de_bord(request, magasin_id):
    """Affiche le tableau de bord de la maison mère."""
    magasin = Magasin.objects.get(id=magasin_id)
    stats = vente_service.get_dashboard_stats()
    return render(request, 'gestion/tableau_de_bord.html', {'magasin': magasin, 'stats': stats})


def modifier_produits_depuis_maison_mere(request, magasin_id):
    """Page de modification des produits depuis la maison mère."""
    produits = produit_service.get_tous_les_produits()
    return render(request, 'gestion/modifier_produits.html', {
        'produits': produits,
        'magasin_id': magasin_id
    })


@require_POST
def modifier_produit(request, produit_id):
    """Modifie les informations d'un produit."""
    nom = request.POST.get("nom")
    prix = float(request.POST.get("prix"))
    description = request.POST.get("description")
    produit_service.mettre_a_jour_produit(produit_id, nom, prix, description)
    return redirect(request.META.get('HTTP_REFERER', '/'))


def approvisionner_magasin(request, centre_logistique_id):
    """Transfère des produits du centre logistique vers un autre magasin."""
    centre = Magasin.objects.get(id=centre_logistique_id)
    magasins = Magasin.objects.exclude(id=centre_logistique_id)
    produits = Produit.objects.all()
    stock_centre_dict = stock_service.get_stock_dict_for_magasin(centre_logistique_id)

    if request.method == "POST":
        destination_id = int(request.POST.get("destination_magasin_id"))
        messages_list = []
        for produit in produits:
            qte_str = request.POST.get(f"quantite_{produit.id}")
            if qte_str:
                quantite = int(qte_str)
                if quantite > 0:
                    try:
                        stock_service.transferer_stock(
                            produit.id, quantite, centre_logistique_id, destination_id
                        )
                        messages_list.append(f"{quantite}x {produit.nom} transféré.")
                    except ValueError as e:
                        messages_list.append(f"❌ {produit.nom} : {str(e)}")

        request.session['messages'] = messages_list
        return redirect('approvisionner_magasin', centre_logistique_id=centre_logistique_id)

    return render(request, 'gestion/approvisionnement.html', {
        'centre_logistique': centre,
        'magasins': magasins,
        'produits': produits,
        'stock_centre_dict': stock_centre_dict,
    })
