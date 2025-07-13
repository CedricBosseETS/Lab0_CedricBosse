import json
import structlog
from warnings import filters as warnings_filters
from django.http import JsonResponse
from django.db.models import Sum, F, ExpressionWrapper, FloatField, Q
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from rest_framework import status, viewsets, filters

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

# Nouveaux imports pour le cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache

from .models import Stock
from produit_service.models import Produit
from .serializers import (
    StockSerializer
)
from caisse.services import magasin_service
from .services import stock_service

logger = structlog.get_logger()

@csrf_exempt
@api_view(['POST'])
def reapprovisionner_api(request, magasin_id):
    magasin = magasin_service.get_magasin_by_id(magasin_id)
    centre_logistique = magasin_service.get_centre_logistique()

    produit_id = request.data.get('produit_id')
    quantite = request.data.get('quantite')

    # Validation basique
    if not produit_id or not quantite:
        return Response({"error": "Produit et quantité sont requis."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        produit = Produit.objects.get(id=produit_id)
    except Produit.DoesNotExist:
        return Response({"error": "Produit invalide."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        quantite = int(quantite)
        if quantite <= 0:
            return Response({"error": "La quantité doit être un entier positif."}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({"error": "La quantité doit être un entier."}, status=status.HTTP_400_BAD_REQUEST)

    # Vérifier que le produit existe dans le stock du centre logistique avec assez de stock
    stock_centre = stock_service.get_stock_entry(centre_logistique.id, produit_id)
    if not stock_centre or stock_centre.quantite < quantite:
        return Response({"error": "Stock insuffisant au centre logistique."}, status=status.HTTP_400_BAD_REQUEST)

    # Transaction atomique pour le transfert de stock
    try:
        with transaction.atomic():
            success, msg = stock_service.transferer_stock(
                produit_id,
                quantite,
                centre_logistique.id,
                magasin.id
            )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"success": msg}, status=status.HTTP_201_CREATED)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def transferer_stock(request):
    logger.info("transferer_stock_start", user=request.user.username, data=request.data)
    centre = magasin_service.get_centre_logistique()
    dest_id = request.data.get('magasin_id')
    produits = request.data.get('produits', [])
    errors, messages = [], []
    for p in produits:
        try:
            pid = int(p.get('produit_id'))
            qty = int(p.get('quantite'))
            success, msg = stock_service.transferer_stock(
                produit_id=pid,
                quantite=qty,
                source_magasin_id=centre.id,
                destination_magasin_id=int(dest_id)
            )
            messages.append(msg)
        except ValueError as ve:
            errors.append(str(ve))
        except Exception as e:
            errors.append(str(e))
    status_code = status.HTTP_200_OK if not errors else status.HTTP_400_BAD_REQUEST
    payload = {"details": messages} if not errors else {"error": errors}
    logger.info("transferer_stock_end", status_code=status_code, errors=errors)
    return Response(payload, status=status_code)

@csrf_exempt
@api_view(['POST'])
def bulk_reapprovisionner_api(request, magasin_id):
    magasin = magasin_service.get_magasin_by_id(magasin_id)
    centre_logistique = magasin_service.get_centre_logistique()

    items = request.data.get('items')
    if not items or not isinstance(items, list):
        return Response({"error": "Une liste 'items' est requise."}, status=status.HTTP_400_BAD_REQUEST)

    messages = []
    erreurs = []

    try:
        with transaction.atomic():
            for item in items:
                produit_id = item.get('produit_id')
                quantite = item.get('quantite')

                if not produit_id or not quantite:
                    erreurs.append(f"Entrée invalide : {item}")
                    continue

                try:
                    produit = Produit.objects.get(id=produit_id)
                    quantite = int(quantite)
                    if quantite <= 0:
                        raise ValueError("Quantité non positive.")
                except Exception as e:
                    erreurs.append(f"Produit {produit_id} : {str(e)}")
                    continue

                stock_centre = stock_service.get_stock_entry(centre_logistique.id, produit_id)
                if not stock_centre or stock_centre.quantite < quantite:
                    erreurs.append(f"Stock insuffisant pour le produit {produit.nom}")
                    continue

                success, msg = stock_service.transferer_stock(
                    produit_id,
                    quantite,
                    centre_logistique.id,
                    magasin.id
                )
                messages.append(msg)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    response = {"success": messages}
    if erreurs:
        response["warnings"] = erreurs

    return Response(response, status=status.HTTP_200_OK)