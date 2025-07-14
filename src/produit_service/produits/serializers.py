from rest_framework import serializers
from produit_service.produits.models import Produit

class ProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = ['id', 'nom', 'prix', 'description']

