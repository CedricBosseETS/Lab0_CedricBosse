from django.db import transaction
from django.db.models import F, Sum, FloatField
from django.utils.timezone import now, timedelta
from vente_service.models import Vente, VenteProduit
from produit_service.models import Produit
from stock_service.models import Stock
from caisse.models import Magasin

@transaction.atomic
def creer_vente(panier: dict, magasin_id: int) -> float:
    """
    Crée une vente à partir du panier.
    Panier : dict {produit_id (str): quantite (int)}
    """
    total = 0
    produits_ids = [int(pid) for pid in panier.keys()]
    
    # Verrouillage des produits et stocks pour éviter les problèmes de concurrence
    produits = Produit.objects.select_for_update().filter(id__in=produits_ids)
    stocks = Stock.objects.select_for_update().filter(magasin_id=magasin_id, produit_id__in=produits_ids)
    
    produit_dict = {str(p.id): p for p in produits}
    stock_dict = {str(s.produit_id): s for s in stocks}

    # Calcul du total et vérification des stocks
    for produit_id_str, quantite in panier.items():
        produit = produit_dict.get(produit_id_str)
        stock = stock_dict.get(produit_id_str)

        if not produit or not stock:
            raise Exception(f"Produit ID {produit_id_str} introuvable ou non en stock.")

        if stock.quantite < quantite:
            raise Exception(f"Stock insuffisant pour {produit.nom}. Disponible : {stock.quantite}")

        total += produit.prix * quantite

    magasin = Magasin.objects.get(id=magasin_id)
    vente = Vente.objects.create(magasin=magasin, total=total)

    lignes = []
    for produit_id_str, quantite in panier.items():
        produit = produit_dict[produit_id_str]
        stock = stock_dict[produit_id_str]

        lignes.append(VenteProduit(
            vente=vente,
            produit=produit,
            quantite=quantite,
            prix_unitaire=produit.prix
        ))

        # Mise à jour du stock avec F() pour éviter les conditions de course
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
    return (
        Vente.objects
        .values('magasin__id', 'magasin__nom')
        .annotate(total_ventes=Sum('total'))
        .order_by('-total_ventes')
    )


def get_produits_les_plus_vendus():
    return (
        VenteProduit.objects
        .values('produit__id', 'produit__nom')
        .annotate(total_vendus=Sum('quantite'))
        .order_by('-total_vendus')[:3]
    )


def get_dashboard_stats():
    today = now().date()
    week_ago = today - timedelta(days=7)

    ventes_par_magasin = (
        Vente.objects
        .values('magasin__id', 'magasin__nom')
        .annotate(total_ventes=Sum('total'))
        .order_by('-total_ventes')
    )

    rupture_stock = (
        Stock.objects
        .filter(quantite__lte=10)
        .select_related('produit', 'magasin')
    )
    surstock = (
        Stock.objects
        .filter(quantite__gt=100)
        .select_related('produit', 'magasin')
    )

    ventes_hebdo = (
        Vente.objects
        .filter(date_heure__date__gte=week_ago)
        .values('date_heure__date')
        .annotate(total=Sum('total'))
        .order_by('date_heure__date')
    )

    return {
        "ventes_par_magasin": list(ventes_par_magasin),
        "rupture_stock": list(rupture_stock),
        "surstock": list(surstock),
        "ventes_hebdo": list(ventes_hebdo),
    }


def get_ventes_pour_maison_mere(maison_id: int) -> list[dict]:
    """
    Retourne la liste des ventes agrégées par magasin pour une maison mère donnée.
    On considère tous les magasins de type 'magasin'.
    """
    qs = (
        Vente.objects
        .filter(magasin__type='magasin')
        .values('magasin__id', 'magasin__nom')
        .annotate(montant=Sum('total', output_field=FloatField()))
        .order_by('-montant')
    )
    return list(qs)
