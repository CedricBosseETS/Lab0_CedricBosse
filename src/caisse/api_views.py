import json
import structlog
from warnings import filters as warnings_filters
from django.http import JsonResponse
from django.db.models import Sum, F, ExpressionWrapper, FloatField
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
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
from django.db.models import Q

# Nouveaux imports pour le cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache

from caisse.services import stock_service, magasin_service, vente_service, produit_service, panier_service

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
'''
'''
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
'''
'''
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
'''
'''
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
'''
'''
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
'''
'''
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
'''

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def approvisionner(request, centre_id):
    destination_id = request.POST.get('destination_magasin_id')

    if not destination_id:
        return Response({"error": "Magasin de destination requis."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        Magasin.objects.get(id=destination_id)
    except Magasin.DoesNotExist:
        return Response({"error": "Magasin de destination invalide."}, status=status.HTTP_404_NOT_FOUND)

    messages = []
    erreurs = []
    for key, value in request.POST.items():
        if key.startswith("quantite_"):
            try:
                produit_id = int(key.replace("quantite_", ""))
                quantite = int(value)
                if quantite > 0:
                    success, msg = stock_service.transferer_stock(
                        produit_id=produit_id,
                        quantite=quantite,
                        source_magasin_id=centre_id,
                        destination_magasin_id=int(destination_id)
                    )
                    messages.append(msg)
            except ValueError as ve:
                erreurs.append(str(ve))
            except Exception as e:
                erreurs.append(f"Erreur pour le produit {produit_id} : {str(e)}")

    if erreurs:
        return Response({"error": erreurs}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"message": "Approvisionnement terminé avec succès.", "details": messages}, status=status.HTTP_200_OK)
'''
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
'''
'''
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
'''
'''
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
'''
'''
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
'''

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