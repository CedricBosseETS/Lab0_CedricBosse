"""
Migration initiale pour l'application caisse.

Cette migration crée les modèles suivants :
- Magasin
- Produit
- Stock
- Vente
- VenteProduit
"""
from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=100)),
                ('prix', models.FloatField()),
                ('description', models.TextField(blank=True)),
            ],
        ),
    ]