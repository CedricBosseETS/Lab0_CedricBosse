from rest_framework import serializers
from produit_service.serializers import ProduitSerializer
from .models import Stock

class StockSerializer(serializers.ModelSerializer):
    produit = ProduitSerializer()

    class Meta:
        model = Stock
        fields = ['id', 'produit', 'quantite', 'magasin']


