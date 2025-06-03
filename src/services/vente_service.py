from django.db import transaction
from django.db.models import F
from caisse.models import Vente, VenteProduit, Produit, Stock, Magasin
from django.db.models import Sum

@transaction.atomic
def creer_vente(panier: dict, magasin_id: int) -> float:
    """
    Crée une vente à partir du panier.
    Panier : dict {produit_id (str): quantite (int)}
    """
    total = 0
    produits_ids = [int(pid) for pid in panier.keys()]
    produits = Produit.objects.select_for_update().filter(id__in=produits_ids)
    stocks = Stock.objects.select_for_update().filter(magasin_id=magasin_id, produit_id__in=produits_ids)
    
    produit_dict = {str(p.id): p for p in produits}
    stock_dict = {f"{s.produit_id}": s for s in stocks}

    # Calculer total et vérifier les stocks
    for produit_id_str, quantite in panier.items():
        produit = produit_dict.get(produit_id_str)
        stock = stock_dict.get(produit_id_str)

        if not produit or not stock:
            raise Exception(f"Produit ID {produit_id_str} introuvable ou non en stock.")

        if stock.quantite < quantite:
            raise Exception(f"Stock insuffisant pour {produit.nom}. Disponible : {stock.quantite}")

        total += produit.prix * quantite

    # Création de la vente
    magasin = Magasin.objects.get(id=magasin_id)
    vente = Vente.objects.create(magasin=magasin, total=total)

    # Création des lignes de vente
    lignes = []
    for produit_id_str, quantite in panier.items():
        produit = produit_dict[produit_id_str]
        stock = stock_dict[produit_id_str]

        ligne = VenteProduit(
            vente=vente,
            produit=produit,
            quantite=quantite,
            prix_unitaire=produit.prix
        )
        lignes.append(ligne)
        stock.quantite = F('quantite') - quantite
        stock.save()

    VenteProduit.objects.bulk_create(lignes)
    return total

@transaction.atomic
def annuler_vente(magasin_id: int, vente_id: int):
    """
    Annule une vente : supprime la vente et remet les produits dans le stock.
    """
    vente = Vente.objects.select_for_update().get(id=vente_id, magasin_id=magasin_id)
    vente_produits = VenteProduit.objects.select_related('produit').filter(vente=vente)

    for vp in vente_produits:
        stock, _ = Stock.objects.select_for_update().get_or_create(
            magasin_id=magasin_id,
            produit=vp.produit,
            defaults={'quantite': 0}
        )
        stock.quantite = F('quantite') + vp.quantite
        stock.save()

    vente.delete()

def get_ventes_par_magasin():
    ventes = (
        Vente.objects
        .values('magasin__id', 'magasin__nom')
         .annotate(total_ventes=Sum('total'))
        .order_by('-total_ventes')
    )
    return ventes

def get_produits_les_plus_vendus():
    produits = (
        VenteProduit.objects
        .values('produit__id', 'produit__nom')
        .annotate(total_vendus=Sum('quantite'))
        .order_by('-total_vendus')[:3]
    )
    return produits