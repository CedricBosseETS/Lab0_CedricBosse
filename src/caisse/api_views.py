import json
from django.http import JsonResponse
from requests import Response
from rest_framework import viewsets
from .models import Magasin, Produit, Stock, Vente
from .serializers import (
    MagasinSerializer,
    ProduitSerializer,
    StockSerializer,
    VenteSerializer
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from caisse.services import stock_service, magasin_service
from caisse.models import Produit

class MagasinViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Magasin.objects.filter(type='magasin')
    serializer_class = MagasinSerializer

class ProduitViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer

class StockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Stock.objects.select_related('magasin', 'produit')
    serializer_class = StockSerializer

class VenteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Vente.objects.select_related('magasin').prefetch_related('venteproduit_set__produit')
    serializer_class = VenteSerializer

class StockViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StockSerializer

    def get_queryset(self):
        queryset = Stock.objects.select_related('produit')
        magasin_id = self.request.query_params.get('magasin_id')
        if magasin_id is not None:
            queryset = queryset.filter(magasin_id=magasin_id)
        return queryset
    
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
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

    return Response({"success": msg})
