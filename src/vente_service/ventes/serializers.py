from rest_framework import serializers
from .models import Vente, VenteProduit


class VenteProduitSerializer(serializers.ModelSerializer):

    class Meta:
        model = VenteProduit
        fields = ['produit_id', 'quantite', 'prix_unitaire']

class VenteSerializer(serializers.ModelSerializer):
    produits = VenteProduitSerializer(source='venteproduit_set', many=True, read_only=True)

    class Meta:
        model = Vente
        fields = ['id', 'date_heure', 'total', 'magasin_id', 'produits']
