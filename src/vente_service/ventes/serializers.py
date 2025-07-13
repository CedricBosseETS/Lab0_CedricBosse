from rest_framework import serializers
from .models import Vente, VenteProduit
from caisse.serializers import MagasinSerializer
from produit_service.produits.serializers import ProduitSerializer

class VenteProduitSerializer(serializers.ModelSerializer):
    produit = ProduitSerializer()

    class Meta:
        model = VenteProduit
        fields = ['produit', 'quantite', 'prix_unitaire']

class VenteSerializer(serializers.ModelSerializer):
    produits = VenteProduitSerializer(source='venteproduit_set', many=True, read_only=True)
    magasin = MagasinSerializer()

    class Meta:
        model = Vente
        fields = ['id', 'date_heure', 'total', 'magasin', 'produits']
