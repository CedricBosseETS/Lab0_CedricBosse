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
