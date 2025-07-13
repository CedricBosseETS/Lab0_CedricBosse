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

from produit_service.produits.models import Produit

from .services import panier_service

logger = structlog.get_logger()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def afficher_panier(request, magasin_id):
    panier = request.session.get("panier", {})
    magasin_id_str = str(magasin_id)

    logger.info("Session panier: %s", panier)

    # Vérifie que le magasin a un panier
    magasin_panier = panier.get(magasin_id_str, {})
    if not isinstance(magasin_panier, dict):
        return Response([])

    produit_ids = list(map(int, magasin_panier.keys()))
    produits = Produit.objects.filter(id__in=produit_ids)

    resultat = []
    for produit in produits:
        resultat.append({
            "produit_id": produit.id,
            "nom": produit.nom,
            "prix": float(produit.prix),
            "quantite": magasin_panier[str(produit.id)]
        })

    return Response(resultat)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ajouter_au_panier(request, magasin_id):
    try:
        data = json.loads(request.body)
        produit_id = data.get("produit_id")
        quantite = data.get("quantite")

        if not produit_id or not quantite:
            return Response({"error": "Champs requis manquants."}, status=400)

        panier_service.ajouter_au_panier(request.session, magasin_id, produit_id=produit_id, quantite=int(quantite))

        return Response({"message": "Produit ajouté au panier."}, status=200)

    except json.JSONDecodeError:
        return Response({"error": "Format JSON invalide."}, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def retirer_du_panier(request, magasin_id):
    try:
        logger.info("Corps brut : %s", request.body)
        logger.info("Content-Type : %s", request.content_type)

        data = request.data
        produit_id = data.get("produit_id")
        if produit_id is None:
            return Response({"error": "produit_id manquant"}, status=400)

        logger.info("Session panier", panier=request.session.get("panier", {}))
        panier_service.retirer_du_panier(request.session, magasin_id, produit_id)
        return Response({"message": "Produit retiré du panier"})
    except Exception as e:
        logger.exception("Erreur lors du retrait du panier")
        return Response({"error": str(e)}, status=500)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def vider_panier(request, magasin_id):
    panier_service.vider_panier(request.session, magasin_id)
    return Response({"message": "Panier vidé."})