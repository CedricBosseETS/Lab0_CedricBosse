import json
import structlog
from warnings import filters as warnings_filters
from django.http import JsonResponse
from django.db.models import Sum, F, ExpressionWrapper, FloatField
from rest_framework import status, viewsets, filters
from .models import Magasin, Produit, Stock, Vente, VenteProduit
from .serializers import (
    MagasinSerializer,
    ProduitSerializer,
    StockSerializer,
    VenteSerializer
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

# Nouveaux imports pour le cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from caisse.services import stock_service, magasin_service, vente_service, produit_service

logger = structlog.get_logger()


class MagasinViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Magasin.objects.filter(type='magasin')
    serializer_class = MagasinSerializer

    def list(self, request, *args, **kwargs):
        logger.info("magasin_list_start", user=request.user.username, params=request.query_params)
        resp = super().list(request, *args, **kwargs)
        logger.info("magasin_list_end", count=len(resp.data), status_code=resp.status_code)
        return resp


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
    @method_decorator(cache_page(120), name="list")
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_panier(request, magasin_id):
    logger.info("get_panier_start", user=request.user.username, magasin_id=magasin_id)
    panier = stock_service.get_panier(magasin_id)
    serializer = StockSerializer(panier, many=True)
    logger.info("get_panier_end", count=len(serializer.data))
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ajouter_au_panier(request, magasin_id):
    logger.info("ajouter_au_panier_start", user=request.user.username, magasin_id=magasin_id, data=request.data)
    produit_id = request.data.get('produit_id')
    quantite = request.data.get('quantite')
    try:
        panier = stock_service.ajouter_au_panier(magasin_id, produit_id, quantite)
    except Exception as e:
        logger.error("ajouter_au_panier_error", error=str(e))
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    serializer = StockSerializer(panier, many=True)
    logger.info("ajouter_au_panier_end", count=len(serializer.data))
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def retirer_du_panier(request, magasin_id):
    logger.info("retirer_du_panier_start", user=request.user.username, magasin_id=magasin_id, data=request.data)
    produit_id = request.data.get('produit_id')
    quantite = request.data.get('quantite')
    try:
        panier = stock_service.retirer_du_panier(magasin_id, produit_id, quantite)
    except Exception as e:
        logger.error("retirer_du_panier_error", error=str(e))
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    serializer = StockSerializer(panier, many=True)
    logger.info("retirer_au_panier_end", count=len(serializer.data))
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def finaliser_vente(request, magasin_id):
    logger.info("finaliser_vente_start", user=request.user.username, magasin_id=magasin_id)
    panier = stock_service.get_panier(magasin_id)
    try:
        total = vente_service.creer_vente(panier, magasin_id)
    except Exception as e:
        logger.error("finaliser_vente_error", magasin_id=magasin_id, error=str(e))
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    stock_service.clear_panier(magasin_id)
    logger.info("finaliser_vente_end", magasin_id=magasin_id, total=total)
    return Response({"total": total})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def annuler_vente(request, magasin_id, vente_id):
    logger.info("annuler_vente_start", user=request.user.username, magasin_id=magasin_id, vente_id=vente_id)
    try:
        vente_service.annuler_vente(magasin_id, vente_id)
    except Exception as e:
        logger.error("annuler_vente_error", error=str(e))
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    logger.info("annuler_vente_end", magasin_id=magasin_id, vente_id=vente_id)
    return Response({"message": "Vente annulée"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sales_report(request):
    logger.info("ventes_par_magasin_start", user=request.user.username)
    data = []
    ventes = vente_service.get_ventes_par_magasin()
    for v in ventes:
        data.append({
            "magasin": v['magasin__nom'],
            "total_ventes": float(v['total_ventes'])
        })
    logger.info("ventes_par_magasin_end", count=len(data))
    return Response({"ventes_par_magasin": data})


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@cache_page(120)  # Mise en cache de 2 minutes
def maison_mere_tableau_de_bord(request, magasin_id):
    logger.info("tableau_de_bord_start",
                user=request.user.username if request.user.is_authenticated else "anonymous",
                magasin_id=magasin_id)

    raw_stats = vente_service.get_ventes_pour_maison_mere(maison_id=magasin_id)
    ventes = []
    for stat in raw_stats:
        ventes.append({
            'magasin_id': stat['magasin'].id,
            'magasin_nom': stat['magasin'].nom,
            'ventes_par_magasin': stat.get('ventes_par_magasin', 0),
            'rupture_stock': stat.get('rupture_stock', 0),
            'surstock': stat.get('surstock', 0),
            'ventes_hebdo': stat.get('ventes_hebdo', 0),
        })

    total_ventes = sum(item['ventes_par_magasin'] for item in ventes)
    logger.info("tableau_de_bord_end", ventes_par_magasin_total=total_ventes)

    return Response({"ventes": ventes, "total": total_ventes}, status=status.HTTP_200_OK)


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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def approvisionner(request, maison_mere_id):
    logger.info("approvisionnement_start", user=request.user.username, maison_mere_id=maison_mere_id, data=request.data)
    centre = magasin_service.get_centre_logistique()
    errors, messages = [], []
    for entry in request.data.get('produits', []):
        try:
            pid = entry['produit_id']
            qty = entry['quantite']
            dest_id = entry['destination_magasin_id']
            _, msg = stock_service.transferer_stock(pid, qty, centre.id, dest_id)
            messages.append(msg)
        except Exception as e:
            errors.append(str(e))
    status_code = status.HTTP_200_OK if not errors else status.HTTP_400_BAD_REQUEST
    payload = {"details": messages} if not errors else {"error": errors}
    logger.info("approvisionnement_end", status_code=status_code, errors=errors)
    return Response(payload, status=status_code)
