import json
import structlog
from warnings import filters as warnings_filters
from django.http import JsonResponse
from django.db.models import Sum, F, ExpressionWrapper, FloatField
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from rest_framework import status, viewsets, filters

from caisse.models import Magasin
from caisse.services import magasin_service
from caisse.serializers import MagasinSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
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
    serializer_class = MagasinSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        type_param = self.request.query_params.get("type", None)
        if type_param:
            return Magasin.objects.filter(type=type_param)
        return Magasin.objects.all()

    def list(self, request, *args, **kwargs):
        logger.info("magasin_list_start", user=request.user.username, params=request.query_params)
        resp = super().list(request, *args, **kwargs)
        logger.info("magasin_list_end", count=len(resp.data), status_code=resp.status_code)
        return resp


@api_view(['GET'])
def get_magasins(request):
    """Retourne tous les magasins."""
    logger.info("get_magasins_start")
    
    magasins = magasin_service.get_all_magasins()
    
    magasins_data = [
        {
            "id": m.id,
            "nom": m.nom,
            "quartier": m.quartier,
            "type": m.type,
        }
        for m in magasins
    ]

    logger.info("get_magasins_success", count=len(magasins))
    return Response(magasins_data, status=status.HTTP_200_OK)

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
