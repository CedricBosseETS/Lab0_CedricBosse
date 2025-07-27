from rest_framework import serializers
from .models import Stock

class StockSerializer(serializers.ModelSerializer):
    produit_nom = serializers.CharField(source='produit.nom', read_only=True)
    produit_prix = serializers.FloatField(source='produit.prix', read_only=True)

    class Meta:
        model = Stock
        fields = ['id', 'produit_id', 'magasin_id', 'quantite', 'produit_nom', 'produit_prix']


