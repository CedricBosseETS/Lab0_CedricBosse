import json
from warnings import filters
from django.http import JsonResponse
from django.db.models import Sum, F, ExpressionWrapper, FloatField
from requests import Response
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
from django.db import transaction
from caisse.services import stock_service, magasin_service, vente_service
from caisse.models import Produit

class MagasinViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Magasin.objects.filter(type='magasin')
    serializer_class = MagasinSerializer

class ProduitViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProduitSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nom', 'id']

    def get_queryset(self):
        magasin_id = self.request.query_params.get('magasin_id')
        if magasin_id:
            return Produit.objects.filter(stocks__magasin_id=magasin_id).distinct()
        return Produit.objects.none()

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

def get_panier_key(magasin_id):
    return f'panier_{magasin_id}'


@api_view(['GET'])
def afficher_panier_api(request, magasin_id):
    panier = request.session.get(get_panier_key(magasin_id), {})
    produits = []

    for produit_id, quantite in panier.items():
        try:
            produit = Produit.objects.get(id=produit_id)
            data = ProduitSerializer(produit).data
            data['quantite'] = quantite
            produits.append(data)
        except Produit.DoesNotExist:
            continue

    return Response({'panier': produits})


@api_view(['POST'])
def ajouter_au_panier_api(request, magasin_id):
    produit_id = str(request.data.get('produit_id'))
    quantite = int(request.data.get('quantite', 1))

    try:
        Produit.objects.get(id=produit_id)
    except Produit.DoesNotExist:
        return Response({"error": "Produit introuvable."}, status=status.HTTP_404_NOT_FOUND)

    panier_key = get_panier_key(magasin_id)
    panier = request.session.get(panier_key, {})

    panier[produit_id] = panier.get(produit_id, 0) + quantite
    request.session[panier_key] = panier
    request.session.modified = True

    return Response({"message": f"{quantite} ajouté(s) au panier."})


@api_view(['POST'])
def retirer_du_panier_api(request, magasin_id):
    produit_id = str(request.data.get('produit_id'))
    quantite = int(request.data.get('quantite', 1))
    panier_key = get_panier_key(magasin_id)
    panier = request.session.get(panier_key, {})

    if produit_id in panier:
        if panier[produit_id] > quantite:
            panier[produit_id] -= quantite
        else:
            del panier[produit_id]
        request.session[panier_key] = panier
        request.session.modified = True
        return Response({"message": f"{quantite} unité(s) retirée(s) du produit {produit_id}."})
    else:
        return Response({"error": "Produit non présent dans le panier."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def finaliser_vente_api(request, magasin_id):
    panier_key = get_panier_key(magasin_id)
    panier = request.session.get(panier_key, {})

    if not panier:
        return Response({"error": "Le panier est vide."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        total = vente_service.creer_vente(panier, magasin_id)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # Vider le panier
    request.session[panier_key] = {}
    request.session.modified = True

    return Response({
        "message": "Vente enregistrée avec succès.",
        "total": total
    }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
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

@api_view(['DELETE'])
def annuler_vente_api(request, magasin_id, vente_id):
    try:
        vente_service.annuler_vente(magasin_id=magasin_id, vente_id=vente_id)
        return Response({'message': 'Vente annulée avec succès.'}, status=status.HTTP_200_OK)
    except Vente.DoesNotExist:
        return Response({'error': 'Vente non trouvée.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

def tableau_de_bord_api(request, magasin_id):
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
def donnees_approvisionnement(request, maison_mere_id):
    try:
        maison_mere = Magasin.objects.get(id=maison_mere_id)
    except Magasin.DoesNotExist:
        return Response({"error": "Maison mère introuvable."}, status=status.HTTP_404_NOT_FOUND)

    # Ici tu choisis le bon centre logistique associé à cette maison mère
    centre_logistique = Magasin.objects.filter(type='centre_logistique').first()
    if not centre_logistique:
        return Response({"error": "Centre logistique non trouvé."}, status=status.HTTP_404_NOT_FOUND)

    magasins = Magasin.objects.exclude(id=centre_logistique.id).values('id', 'nom')
    produits = stock_service.get_produits_disponibles(centre_logistique.id)
    stock_dict = stock_service.get_stock_dict_for_magasin(centre_logistique.id)

    print("Produits disponibles:", produits)
    print("Stock dict:", stock_dict)

    data = {
        "centre_id": centre_logistique.id,
        "magasins": list(magasins),
        "produits": [{"id": p.id, "nom": p.nom} for p in produits],
        "stocks": {pid: stock.quantite for pid, stock in stock_dict.items()}
    }
    return Response(data, status=status.HTTP_200_OK)

@api_view(['POST'])
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