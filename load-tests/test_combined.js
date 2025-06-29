import http from 'k6/http';
import { check, sleep } from 'k6';
import encoding from 'k6/encoding';

const BASE_URL = 'http://localhost:5000';
const credentials = encoding.b64encode('super_caisse_user:supersecret');
const authHeaders = {
  Authorization: `Basic ${credentials}`,
  'Content-Type': 'application/json',
};

export let options = {
  scenarios: {
    // Consultation de stock
    consult_stock: {
      executor: 'constant-vus',
      vus: 20,
      duration: '60s',
      exec: 'consultStock',
    },
    // Génération de rapport
    generate_report: {
      executor: 'constant-vus',
      vus: 20,
      duration: '60s',
      exec: 'generateReport',
    },
    // Mise à jour de produit
    update_product: {
      executor: 'constant-vus',
      vus: 20,
      duration: '60s',
      exec: 'updateProduct',
    },
  },
};

export function consultStock() {
  const magasinIds = [1, 2, 3];
  magasinIds.forEach((id) => {
    let res = http.get(
      `${BASE_URL}/api/stocks/?magasin_id=${id}`,
      { headers: authHeaders }
    );

    let body = null;
    if (res.status === 200) {
      try {
        body = res.json();
      } catch {
        body = null;
      }
    }

    check(res, {
      'stock status is 200': (r) => r.status === 200,
      'stock is array': () => Array.isArray(body),
    });
  });

  // même rythme que ton script original
  sleep(0.05);
}

export function generateReport() {
  const magasinId = 7;
  let res = http.get(
    `${BASE_URL}/api/maison_mere/${magasinId}/tableau_de_bord/`,
    { headers: authHeaders }
  );

  let body = {};
  if (res.status === 200) {
    try {
      body = res.json();
    } catch {
      body = {};
    }
  }

  check(res, {
    'status is 200': (r) => r.status === 200,
    'ventes is array': () => Array.isArray(body.ventes),
    'total is number': () => typeof body.total === 'number',
  });

  sleep(0.05);
}

export function updateProduct() {
  const produitId = 1;
  const url = `${BASE_URL}/api/produits/${produitId}/`;
  const payload = JSON.stringify({
    nom: 'Produit Modifié K6',
    prix: 15.99,
    description: 'Mise à jour via K6',
  });

  let res = http.put(url, payload, { headers: authHeaders });

  let body = {};
  if (res.status === 200 || res.status === 204) {
    try {
      body = res.json();
    } catch {
      body = {};
    }
  }

  check(res, {
    'status is 200 or 204': (r) => r.status === 200 || r.status === 204,
    'nom mis à jour': () => body.nom === 'Produit Modifié K6',
    'prix mis à jour': () => body.prix === 15.99,
    'description mise à jour': () => body.description === 'Mise à jour via K6',
  });

  sleep(0.05);
}
