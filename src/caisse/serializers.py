from rest_framework import serializers
from .models import Magasin, Produit, Stock, Vente, VenteProduit

class MagasinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Magasin
        fields = '__all__'

class ProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = ['id', 'nom', 'prix', 'description']

class StockSerializer(serializers.ModelSerializer):
    produit = ProduitSerializer()

    class Meta:
        model = Stock
        fields = ['id', 'produit', 'quantite', 'magasin']

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
