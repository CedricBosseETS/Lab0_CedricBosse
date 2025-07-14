import json
import structlog
from warnings import filters as warnings_filters
from django.http import JsonResponse
from django.db.models import Sum, F, ExpressionWrapper, FloatField
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from rest_framework import status, viewsets, filters

from caisse.models import Magasin

from caisse.serializers import MagasinSerializer

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

logger = structlog.get_logger()

class MagasinViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Magasin.objects.filter(type='magasin')
    serializer_class = MagasinSerializer

    def list(self, request, *args, **kwargs):
        logger.info("magasin_list_start", user=request.user.username, params=request.query_params)
        resp = super().list(request, *args, **kwargs)
        logger.info("magasin_list_end", count=len(resp.data), status_code=resp.status_code)
        return resp

@api_view(['GET'])
def get_magasin_by_id(request, id):
    """Retourne un magasin par ID."""
    logger.info("get_magasin_by_id_start", magasin_id=id, user=str(request.user))
    magasin = get_object_or_404(Magasin, id=id)
    serializer = MagasinSerializer(magasin)
    logger.info("get_magasin_by_id_success", magasin_id=id)
    return Response(serializer.data, status=200)

@api_view(['GET'])
def get_centre_logistique(request):
    """Retourne le centre logistique (type='logistique')."""
    logger.info("get_centre_logistique_start", user=str(request.user))
    try:
        centre = Magasin.objects.get(type='logistique')
        serializer = MagasinSerializer(centre)
        logger.info("get_centre_logistique_success", centre_id=centre.id)
        return Response(serializer.data, status=200)
    except Magasin.DoesNotExist:
        logger.warning("get_centre_logistique_not_found")
        return Response({"error": "Centre logistique non trouvé"}, status=404)

'''
class ProduitViewSet(viewsets.ModelViewSet):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nom', 'description', 'id']

    def list(self, request, *args, **kwargs):
        logger.info("produit_list_start", user=request.user.username, params=request.query_params)
        resp = super().list(request, *args, **kwargs)
        logger.info("produit_list_end", count=len(resp.data), status_code=resp.status_code)
        return resp

    def update(self, request, *args, **kwargs):
        produit_id = kwargs.get('pk')
        logger.info("produit_update_start", user=request.user.username, produit_id=produit_id, data=request.data)
        nom = request.data.get('nom')
        prix = request.data.get('prix')
        description = request.data.get('description')
        if not all([nom, prix, description]):
            logger.warning("produit_update_missing_fields", produit_id=produit_id)
            return Response({"error": "nom, prix et description sont requis."},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            produit = produit_service.mettre_a_jour_produit(
                produit_id=int(produit_id), nom=nom, prix=float(prix), description=description
            )
        except Produit.DoesNotExist:
            logger.error("produit_not_found", produit_id=produit_id)
            return Response({"error": "Produit non trouvé."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error("produit_update_error", produit_id=produit_id, error=str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(produit)
        logger.info("produit_update_end", produit_id=produit_id)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Stock.objects.select_related('produit', 'magasin')
    serializer_class = StockSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        magasin_id = self.request.query_params.get('magasin_id')
        if magasin_id:
            return qs.filter(magasin_id=magasin_id)
        return qs.none()

    # Mise en cache de 2 minutes (120s) de la liste
    @method_decorator(cache_page(60), name="list")
    def list(self, request, *args, **kwargs):
        logger.info("stock_list_start", user=request.user.username, params=request.query_params)
        resp = super().list(request, *args, **kwargs)
        logger.info("stock_list_end", count=len(resp.data), status_code=resp.status_code)
        return resp


class VenteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Vente.objects.select_related('magasin').prefetch_related('venteproduit_set__produit')
    serializer_class = VenteSerializer

    def list(self, request, *args, **kwargs):
        logger.info("vente_list_start", user=request.user.username)
        resp = super().list(request, *args, **kwargs)
        logger.info("vente_list_end", count=len(resp.data), status_code=resp.status_code)
        return resp
'''