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
        url = f"/api/magasins/{self.magasin.id}/panier/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_ajouter_au_panier(self):
        url = f"/api/magasins/{self.magasin.id}/panier/ajouter/"
        data = {"produit_id": self.produit.id, "quantite": 2}
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertIn(response.status_code, [200, 201])
        self.assertIn("message", response.json())

    def test_retirer_du_panier(self):
        # Ajouter avant de retirer (sinon panier vide)
        self.client.post(
            f"/api/magasins/{self.magasin.id}/panier/ajouter/",
            data=json.dumps({"produit_id": self.produit.id, "quantite": 1}),
            content_type="application/json"
        )

        # Retirer le produit
        url = f"/api/magasins/{self.magasin.id}/panier/retirer/"
        data = {"produit_id": self.produit.id}
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())

    def test_finaliser_vente(self):
        # Ajouter un produit au panier avant de finaliser
        self.client.post(
            f"/api/magasins/{self.magasin.id}/panier/ajouter/",
            data=json.dumps({
                "produit_id": self.produit.id,
                "quantite": 2
            }),
            content_type="application/json"
        )

        # Finaliser la vente
        url = f"/api/magasins/{self.magasin.id}/panier/finaliser/"
        response = self.client.post(url)

        self.assertIn(response.status_code, [200, 201])

    def test_annuler_vente(self):
        # Ajouter un produit au panier
        self.client.post(
            f"/api/magasins/{self.magasin.id}/panier/ajouter/",
            data=json.dumps({
                "produit_id": self.produit.id,
                "quantite": 1
            }),
            content_type="application/json"
        )

        # Finaliser la vente
        self.client.post(f"/api/magasins/{self.magasin.id}/panier/finaliser/")

        # Récupérer la vente créée
        vente = Vente.objects.filter(magasin=self.magasin).last()

        # Annuler la vente
        url = f"/api/panier/{self.magasin.id}/annuler/{vente.id}/"
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())




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

    def test_reapprovisionner_api(self):
        centre_logistique = Magasin.objects.create(nom="Centre Logistique", type="logistique")
        produit = Produit.objects.create(nom="Produit Test", prix=10.0)
        Stock.objects.create(magasin=centre_logistique, produit=produit, quantite=50)

        url = f"/api/magasins/{self.magasin.id}/reapprovisionner/"
        data = {
            "produit_id": produit.id,
            "quantite": 10
        }

        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type="application/json"
        )

        self.assertIn(response.status_code, [200, 201])
        self.assertIn("success", response.json())


    #def test_bulk_approvisionnement(self): to fix
