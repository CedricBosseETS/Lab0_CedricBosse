from django.shortcuts import render
from services import magasin_service, vente_service, stock_service

def admin_page(request):
    magasins = magasin_service.get_all_magasins()
    entites_admin = [m for m in magasins if m.type != 'magasin']
    return render(request, 'gestion.html', {'entites_admin': entites_admin})

def admin_entite(request, magasin_id):
    magasin = magasin_service.get_magasin_by_id(magasin_id)
    if magasin.type == 'admin':
        return render(request, 'gestion/maison_mere.html', {'magasin': magasin})
    else:
        # Rediriger vers une autre interface plus simple pour centre logistique ou autre
        return render(request, 'gestion/centre_logistique.html', {'magasin': magasin})
    
def rapport_ventes(request, magasin_id):
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
