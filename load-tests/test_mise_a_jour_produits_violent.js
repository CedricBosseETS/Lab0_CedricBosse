import http from 'k6/http';
import { check, sleep } from 'k6';
import encoding from 'k6/encoding';

export const options = {
  vus: 200,
  duration: '60s',
};

export default function () {
  // ID du produit à mettre à jour
  const produitId = 1;
  const url = `http://localhost:5000/api/produits/${produitId}/`;

  // Encodage des credentials Basic Auth
  const credentials = encoding.b64encode('super_caisse_user:supersecret');

  // Payload JSON — n'inclut que les champs gérés par l'API
  const payload = JSON.stringify({
    nom: 'Produit Modifié K6',
    prix: 15.99,
    description: 'Mise à jour via K6'
  });

  const params = {
    headers: {
      'Authorization': `Basic ${credentials}`,
      'Content-Type': 'application/json',
    },
    // en cas de cookies ou session, sinon omit
    credentials: 'include',
  };

  // Exécution de la requête PUT
  const res = http.put(url, payload, params);

  // Vérifications
  check(res, {
    'status is 200': (r) => r.status === 200,
    'nom mis à jour': (r) => r.json('nom') === 'Produit Modifié K6',
    'prix mis à jour': (r) => parseFloat(r.json('prix')) === 15.99,
    'description mise à jour': (r) => r.json('description') === 'Mise à jour via K6',
  });

  sleep(0.05);
}