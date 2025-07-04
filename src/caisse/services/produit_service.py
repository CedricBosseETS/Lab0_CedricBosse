"""Ce module gère les accès à la base de données pour tout ce qui concerne les produits."""
from django.db.models import Q
from caisse.models import Stock, Produit

def get_produits_par_magasin(magasin_id):
    """Retourne la liste des produits disponibles dans un magasin donné."""
    stocks = Stock.objects.filter(magasin_id=magasin_id).select_related('produit')
    return [stock.produit for stock in stocks]

def rechercher_produits_par_nom_ou_id(query):
    """Recherche des produits par ID exact ou par nom partiel."""
    if query.isdigit():
        return Produit.objects.filter(Q(id=int(query)) | Q(nom__icontains=query))
    return Produit.objects.filter(nom__icontains=query)

def get_tous_les_produits():
    """Retourne tous les produits."""
    return Produit.objects.all()

def mettre_a_jour_produit(produit_id: int, nom: str, prix: float, description: str):
    """Met à jour un produit existant."""
    produit = Produit.objects.get(id=produit_id)
    produit.nom = nom
    produit.prix = prix
    produit.description = description
    produit.save()
    return produit
