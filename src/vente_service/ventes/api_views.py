import json
import structlog
from warnings import filters as warnings_filters
from django.http import JsonResponse
from django.db.models import Sum, F, ExpressionWrapper, FloatField
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from rest_framework import status, viewsets, filters
from .models import Vente, VenteProduit
from .serializers import (
    VenteSerializer
)
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

from .services import vente_service
from panier_service.panier.services import panier_service

logger = structlog.get_logger()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ventes_par_magasin_api(request, magasin_id):
    ventes = Vente.objects.filter(magasin_id=magasin_id).order_by('-date_heure')
    data = []

    for vente in ventes:
        vente_data = {
            "id": vente.id,
            "date": vente.date_heure.strftime("%Y-%m-%d %H:%M:%S"),
            "total": float(vente.total),
            "produits": [
                {
                    "nom": vp.produit.nom,
                    "quantite": vp.quantite
                } for vp in vente.produits.all()
            ]
        }
        data.append(vente_data)

    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def finaliser_vente(request, magasin_id):
    logger.info("finaliser_vente_start", user=request.user.username, magasin_id=magasin_id)
    panier = panier_service.get_panier(request.session, magasin_id)
    try:
        total = vente_service.creer_vente(panier, magasin_id)
    except Exception as e:
        logger.error("finaliser_vente_error", error=str(e))
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    panier_service.vider_panier(request.session, magasin_id)
    logger.info("finaliser_vente_end", magasin_id=magasin_id, total=total)
    return Response({"total": total}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def annuler_vente(request, magasin_id, vente_id):
    logger.info("annuler_vente_start", user=request.user.username,
                magasin_id=magasin_id, vente_id=vente_id)
    try:
        vente_service.annuler_vente(magasin_id, vente_id)
    except Exception as e:
        logger.error("annuler_vente_error", error=str(e))
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    logger.info("annuler_vente_end", magasin_id=magasin_id, vente_id=vente_id)
    return Response({"message": "Vente annulée"}, status=status.HTTP_200_OK)