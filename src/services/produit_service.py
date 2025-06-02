"""Ce module s'occupe de gérer les accès à la DB pour tout ce qui touche aux produits"""
from caisse.models import Stock, Produit

def get_produits_par_magasin(magasin_id):
    stocks = Stock.objects.filter(magasin_id=magasin_id).select_related('produit')
    return [stock.produit for stock in stocks]

def rechercher_produits_par_nom_ou_id(query):
    if query.isdigit():
        return Produit.objects.filter(Q(id=int(query)) | Q(nom__icontains=query))
    return Produit.objects.filter(nom__icontains=query)
