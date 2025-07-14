"""
Migration initiale pour l'application caisse.
"""
from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):

    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Vente',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date_heure', models.DateTimeField(default=django.utils.timezone.now)),
                ('total', models.FloatField()),
                ('magasin_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='VenteProduit',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('quantite', models.IntegerField()),
                ('prix_unitaire', models.FloatField()),
                ('produit_id', models.IntegerField()),
                ('vente_id', models.IntegerField()),
            ],
        ),
    ]