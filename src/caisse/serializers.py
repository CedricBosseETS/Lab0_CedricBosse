from rest_framework import serializers
from .models import Magasin, Produit, Stock, Vente, VenteProduit

class MagasinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Magasin
        fields = '__all__'
