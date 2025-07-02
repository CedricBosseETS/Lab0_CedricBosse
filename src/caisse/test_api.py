from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
import base64
from caisse.models import Magasin, Produit, Stock, Vente
import json
from unittest.mock import patch
from django.db import transaction

class APIMagasinsTest(TestCase):
    def setUp(self):
        self.username = "admin"
        self.password = "adminpass"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.defaults['HTTP_AUTHORIZATION'] = self._get_basic_auth_header()

        self.magasin = Magasin.objects.create(nom="Magasin Test", type="magasin")
        self.produit = Produit.objects.create(nom="Produit Test", prix=10.0)
        self.stock = Stock.objects.create(produit=self.produit, magasin=self.magasin, quantite=100)

    def _get_basic_auth_header(self):
        credentials = f"{self.username}:{self.password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded_credentials}"

    def test_get_magasins(self):
        response = self.client.get("/api/magasins/")
        self.assertEqual(response.status_code, 200)

    def test_magasins_unauthorized(self):
        self.client.defaults.pop("HTTP_AUTHORIZATION", None)
        response = self.client.get("/api/magasins/")
        self.assertEqual(response.status_code, 401)

    def _get_basic_auth_header(self):
        credentials = f"{self.username}:{self.password}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded}"

    def test_list_magasins(self):
        response = self.client.get("/api/magasins/")
        self.assertEqual(response.status_code, 200)

    def test_list_produits(self):
        response = self.client.get("/api/produits/")
        self.assertEqual(response.status_code, 200)

    def test_list_stocks(self):
        response = self.client.get("/api/stocks/")
        self.assertEqual(response.status_code, 200)

    def test_afficher_panier(self):
        url = f"/api/panier/{self.magasin.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_ajouter_au_panier(self):
        url = f"/panier/{self.magasin.id}/ajouter/"
        data = {"produit_id": self.produit.id, "quantite": 2}
        response = self.client.post(url, data=json.dumps(data), content_type="application/json")
        self.assertIn(response.status_code, [200, 201])  # dépend de ton implémentation

    def test_retirer_du_panier(self):
        # Ajouter avant de retirer (sinon panier vide)
        self.client.post(f"/panier/{self.magasin.id}/ajouter/", data=json.dumps({
            "produit_id": self.produit.id, "quantite": 1
        }), content_type="application/json")

        url = f"/api/panier/{self.magasin.id}/retirer/"
        data = {"produit_id": self.produit.id}
        response = self.client.post(url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_finaliser_vente(self):
        # Ajouter au panier avant de finaliser
        self.client.post(f"/panier/{self.magasin.id}/ajouter/", data=json.dumps({
            "produit_id": self.produit.id, "quantite": 2
        }), content_type="application/json")

        url = f"/api/panier/{self.magasin.id}/finaliser/"
        response = self.client.post(url)
        self.assertIn(response.status_code, [200, 201])

    def test_ventes_par_magasin(self):
        url = "/api/rapports/ventes/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_annuler_vente(self):
        # Créer une vente pour tester l’annulation
        self.client.post(f"/panier/{self.magasin.id}/ajouter/", data=json.dumps({
            "produit_id": self.produit.id, "quantite": 1
        }), content_type="application/json")
        self.client.post(f"/api/panier/{self.magasin.id}/finaliser/")
        vente = Vente.objects.filter(magasin=self.magasin).last()
        url = f"/api/magasins/{self.magasin.id}/ventes/{vente.id}/annuler/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)


    def test_reapprovisionner(self):
        centre_logistique = Magasin.objects.create(nom="Centre Logistique Test", type="logistique")
        magasin = Magasin.objects.create(nom="Magasin Test", type="magasin")

        produit = Produit.objects.create(nom="Produit Test", prix=10.0)

        Stock.objects.create(magasin=centre_logistique, produit=produit, quantite=100)

        data = {
            'produit_id': produit.id,
            'quantite': 10,
            'destination_magasin_id': magasin.id,
        }

        url = f"/api/magasins/{magasin.id}/reapprovisionner/"

        response = self.client.post(url, data)

        self.assertIn(response.status_code, [200, 201])
        self.assertIn("success", response.json())

    def test_rapport_ventes(self):
        # Création d’un magasin de type admin (maison mère)
        magasin_admin = Magasin.objects.create(nom="Maison Mère Admin", type="admin")

        url = f"/api/maison_mere/{magasin_admin.id}/rapport_ventes/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn("ventes_par_magasin", data)
        self.assertIn("produits_plus_vendus", data)
        self.assertIn("stocks_restant", data)

    def test_tableau_de_bord(self):
        self.magasin.type = "maison_mere"
        self.magasin.save()
        url = f"/api/maison_mere/{self.magasin.id}/tableau_de_bord/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_donnees_approvisionnement(self):
        # Création de la maison mère
        maison_mere = Magasin.objects.create(nom="Maison Mère Test", type="maison_mere")

        # Création du centre logistique
        centre_logistique = Magasin.objects.create(nom="Centre Logistique Test", type="centre_logistique")

        # Mock des fonctions de stock_service pour éviter dépendances sur la DB et logique métier
        with patch('caisse.services.stock_service.get_produits_disponibles') as mock_get_produits, \
            patch('caisse.services.stock_service.get_stock_dict_for_magasin') as mock_get_stock_dict:

            mock_get_produits.return_value = []  # ou liste d’objets Produit simulés
            mock_get_stock_dict.return_value = {}

            url = f"/api/maison_mere/{maison_mere.id}/donnees_approvisionnement/"

            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data['centre_id'], centre_logistique.id)
            self.assertIn('magasins', data)
            self.assertIn('produits', data)
            self.assertIn('stocks', data)

    def test_approvisionner(self):
        centre = Magasin.objects.create(nom="Centre", type="centre_logistique")
        destination = Magasin.objects.create(nom="Magasin C", type="magasin")
        produit = Produit.objects.create(nom="Produit D", prix=12.5)
        Stock.objects.create(magasin=centre, produit=produit, quantite=20)

        url = f"/api/maison_mere/{centre.id}/approvisionner/"
        data = {
            "destination_magasin_id": destination.id,
            f"quantite_{produit.id}": 5
        }

        response = self.client.post(url, data)
        self.assertIn(response.status_code, [200, 201])
        self.assertIn("message", response.json())
