"""Ce module s'occupe de gérer les accès à la DB pour tout ce qui touche aux produits"""
from caisse.models import Stock

def get_produits_par_magasin(magasin_id):
    stocks = Stock.objects.filter(magasin_id=magasin_id).select_related('produit')
    return [stock.produit for stock in stocks]
