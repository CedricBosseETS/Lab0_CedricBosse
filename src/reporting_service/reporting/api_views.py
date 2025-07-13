import json
import structlog
from warnings import filters as warnings_filters
from django.http import JsonResponse
from django.db.models import Sum, F, ExpressionWrapper, FloatField
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from rest_framework import status, viewsets, filters
from caisse.models import Magasin
from produit_service.produits.models import Produit
from stock_service.stocks.models import Stock
from vente_service.ventes.models import Vente, VenteProduit

from caisse.serializers import MagasinSerializer
from produit_service.serializers import ProduitSerializer
from stock_service.serializers import StockSerializer
from vente_service.serializers import VenteSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.db.models import Q

# Nouveaux imports pour le cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache

from caisse.services import magasin_service
from stock_service.stocks.services import stock_service
from produit_service.produits.services import produit_service


logger = structlog.get_logger()

def rapport_ventes_api(request, magasin_id):
    # Vérifie que le magasin est bien la maison mère
    try:
        magasin = Magasin.objects.get(id=magasin_id, type='admin')
    except Magasin.DoesNotExist:
        return JsonResponse({"error": "Magasin introuvable ou non autorisé."}, status=404)

    # 1. Total des ventes par magasin
    ventes_par_magasin_qs = (
        VenteProduit.objects
        .values('vente__magasin__nom')
        .annotate(
            total_ventes=Sum(
                ExpressionWrapper(
                    F('quantite') * F('produit__prix'),
                    output_field=FloatField()
                )
            )
        )
        .order_by('-total_ventes')
    )
    ventes_par_magasin = [
        {"magasin": v["vente__magasin__nom"], "total_ventes": v["total_ventes"] or 0}
        for v in ventes_par_magasin_qs
    ]

    # 2. Produits les plus vendus (toutes ventes confondues)
    produits_plus_vendus_qs = (
        VenteProduit.objects
        .values('produit__nom')
        .annotate(total_vendus=Sum('quantite'))
        .order_by('-total_vendus')[:10]
    )
    produits_plus_vendus = [
        {"nom": p["produit__nom"], "quantite": p["total_vendus"]}
        for p in produits_plus_vendus_qs
    ]

    # 3. Stock total par magasin
    stocks_qs = (
        Stock.objects
        .values('magasin__nom')
        .annotate(stock_total=Sum('quantite'))
    )
    stocks_restant = [
        {"magasin": s["magasin__nom"], "stock": s["stock_total"]}
        for s in stocks_qs
    ]

    return JsonResponse({
        "ventes_par_magasin": ventes_par_magasin,
        "produits_plus_vendus": produits_plus_vendus,
        "stocks_restant": stocks_restant
    })

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@cache_page(120)  # Mise en cache de 2 minutes
def tableau_de_bord_api(request, magasin_id):
    logger.info("tableau_de_bord_start",
            user=request.user.username if request.user.is_authenticated else "anonymous",
            magasin_id=magasin_id)    
    # 1. Chiffre d’affaires par magasin
    ventes_par_magasin = list(
        VenteProduit.objects
        .values('vente__magasin__nom')
        .annotate(total_ventes=Sum(
            ExpressionWrapper(F('quantite') * F('produit__prix'), output_field=FloatField())
        ))
        .order_by('-total_ventes')
    )

    # 2. Produits en rupture de stock (quantité <= 0)
    rupture_stock = list(
        Stock.objects
        .filter(quantite__lte=0)
        .values('produit__nom', 'magasin__nom', 'quantite')
    )

    # 3. Produits en surstock (quantité > 100)
    surstock = list(
        Stock.objects
        .filter(quantite__gt=100)
        .values('produit__nom', 'magasin__nom', 'quantite')
    )

    # 4. Tendances hebdomadaires (ventes regroupées par jour)
    ventes_hebdo = list(
        VenteProduit.objects
        .values('vente__date_heure__date')
        .annotate(total=Sum(
            ExpressionWrapper(F('quantite') * F('produit__prix'), output_field=FloatField())
        ))
        .order_by('vente__date_heure__date')
    )

    return JsonResponse({
        "ventes_par_magasin": ventes_par_magasin,
        "rupture_stock": rupture_stock,
        "surstock": surstock,
        "ventes_hebdo": ventes_hebdo
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def donnees_approvisionnement(request, maison_mere_id):
    logger.info("donnees_approvisionnement_start", user=request.user.username, maison_mere_id=maison_mere_id)
    try:
        Mag = Magasin.objects.get(id=maison_mere_id)
    except Magasin.DoesNotExist:
        logger.error("donnees_approvisionnement_not_found", maison_mere_id=maison_mere_id)
        return Response({"error": "Maison mère introuvable."}, status=status.HTTP_404_NOT_FOUND)
    magasins = magasin_service.get_all_magasins()
    produits = produit_service.get_all_produits()
    stocks = stock_service.get_stock_dict_par_magasin(maison_mere_id)
    data = {
        "magasins": MagasinSerializer(magasins, many=True).data,
        "produits": ProduitSerializer(produits, many=True).data,
        "stocks": stocks
    }
    logger.info("donnees_approvisionnement_end", magasins=len(magasins), produits=len(produits))
    return Response(data)