"""Ce module gère les accès à la base de données pour tout ce qui concerne les stocks."""
from django.db import transaction
from django.db.models import Sum
from caisse.models import Stock, Produit

def _session_key(magasin_id):
    return f"panier_{magasin_id}"

def get_panier(magasin_id, session):
    """
    Récupère le panier (dict produit_id->quantité) depuis la session
    et retourne une liste d'objets Stock fictifs pour la sérialisation.
    """
    panier = session.get(_session_key(magasin_id), {})
    result = []
    for pid_str, qty in panier.items():
        try:
            produit = Produit.objects.get(pk=int(pid_str))
        except Produit.DoesNotExist:
            continue
        # On crée un objet Stock “à la volée” sans l'enregistrer en base
        result.append(Stock(magasin_id=magasin_id, produit=produit, quantite=qty))
    return result

def ajouter_au_panier(magasin_id, produit_id, quantite, session):
    """
    Ajoute ou incrémente la quantité d'un produit dans le panier de session.
    """
    key = _session_key(magasin_id)
    panier = session.get(key, {})
    panier[str(produit_id)] = panier.get(str(produit_id), 0) + int(quantite)
    session[key] = panier
    session.modified = True
    return get_panier(magasin_id, session)

def retirer_du_panier(magasin_id, produit_id, quantite, session):
    """
    Décrémente ou retire un produit du panier de session.
    """
    key = _session_key(magasin_id)
    panier = session.get(key, {})
    pid = str(produit_id)
    if pid not in panier:
        raise ValueError("Produit non présent dans le panier.")
    new_qty = panier[pid] - int(quantite)
    if new_qty > 0:
        panier[pid] = new_qty
    else:
        panier.pop(pid)
    session[key] = panier
    session.modified = True
    return get_panier(magasin_id, session)

def clear_panier(magasin_id, session):
    """
    Vide le panier pour ce magasin dans la session.
    """
    key = _session_key(magasin_id)
    if key in session:
        session.pop(key)
        session.modified = True

def get_stock_total_par_magasin():
    """
    Retourne la quantité totale en stock par magasin sous forme de queryset
    avec magasin id, nom, et somme des quantités.
    """
    stocks = (
        Stock.objects
        .values('magasin__id', 'magasin__nom')
        .annotate(stock_total=Sum('quantite'))
    )
    return stocks

def get_stock_par_magasin(magasin_id):
    """Retourne toutes les entrées de stock pour un magasin donné avec les produits liés."""
    return Stock.objects.filter(magasin_id=magasin_id).select_related('produit')

def get_stock_entry(magasin_id, produit_id):
    """Retourne l'entrée de stock pour un produit donné dans un magasin donné ou None."""
    return Stock.objects.filter(magasin_id=magasin_id, produit_id=produit_id).first()

def get_stock_dict_for_magasin(magasin_id):
    """
    Retourne un dictionnaire indexé par produit_id contenant
    les entrées de stock pour un magasin donné.
    """
    stock_list = Stock.objects.filter(magasin_id=magasin_id).select_related('produit')
    return {stock.produit.id: stock for stock in stock_list}

def get_stock_indexed_by_produit(centre_id, magasin_id):
    """
    Retourne deux dictionnaires indexés par produit_id : stock du centre et stock local.
    """
    stock_centre = get_stock_dict_for_magasin(centre_id)
    stock_local = get_stock_dict_for_magasin(magasin_id)
    return stock_centre, stock_local

def get_produits_disponibles(magasin_id):
    """Retourne la liste des produits avec stock > 0 dans un magasin donné."""
    stock_entries = Stock.objects.filter(magasin_id=magasin_id, quantite__gt=0).select_related('produit')
    return [entry.produit for entry in stock_entries]

@transaction.atomic
def transferer_stock(produit_id, quantite, source_magasin_id, destination_magasin_id):
    """
    Transfère une quantité de produit d'un magasin source vers un magasin destination.
    Utilise select_for_update pour éviter les problèmes de concurrence.
    """
    source_stock = Stock.objects.select_for_update().filter(
        magasin_id=source_magasin_id, produit_id=produit_id
    ).first()

    if not source_stock or source_stock.quantite < quantite:
        raise ValueError("Stock insuffisant au centre logistique.")

    dest_stock, _ = Stock.objects.select_for_update().get_or_create(
        magasin_id=destination_magasin_id, produit_id=produit_id,
        defaults={'quantite': 0}
    )

    source_stock.quantite -= quantite
    dest_stock.quantite += quantite

    source_stock.save()
    dest_stock.save()

    return True, "Transfert effectué avec succès."
