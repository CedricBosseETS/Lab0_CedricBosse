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
            name='Stock',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('quantite', models.IntegerField()),
                ('produit_id', models.IntegerField()),
                ('magasin_id', models.IntegerField()),
            ],
        ),
    ]