import json
import structlog
from warnings import filters as warnings_filters
from django.http import JsonResponse
from django.db.models import Sum, F, ExpressionWrapper, FloatField
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from rest_framework import status, viewsets, filters

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

from .models import Produit
from .serializers import (
    ProduitSerializer
)
from produits.services import produit_service
from stock_service.stocks.services import stock_service

logger = structlog.get_logger()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def rechercher_produits_disponibles(request, magasin_id):
    """
    Recherche de produits disponibles dans un magasin donné (nom ou ID).
    """
    query = request.GET.get('search', '').strip()

    if not query:
        return Response([], status=200)

    produits = Produit.objects.filter(
        Q(nom__icontains=query) | Q(id__icontains=query)
    )

    produits_disponibles = []
    for produit in produits:
        stock = stock_service.get_stock_entry(magasin_id, produit.id)
        if stock and stock.quantite > 0:
            produits_disponibles.append(produit)

    serializer = ProduitSerializer(produits_disponibles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_produit(request, pk):
    try:
        produit = Produit.objects.get(pk=pk)
        serializer = ProduitSerializer(produit)
        return Response(serializer.data)
    except Produit.DoesNotExist:
        return Response(status=404)
'''
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_produit_serializer(request, pk):
    try:
        produit = Produit.objects.get(pk=pk)
        serializer = ProduitSerializer(produit)
        return Response(serializer.data, status=200)
    except Produit.DoesNotExist:
        return Response({'detail': 'Produit non trouvé'}, status=404)
'''