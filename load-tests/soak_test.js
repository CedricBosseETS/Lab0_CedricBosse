import http from 'k6/http';
import { check, sleep } from 'k6';
import encoding from 'k6/encoding';

export const options = {
  scenarios: {
    update_product: {
      executor: 'constant-vus',
      exec: 'updateProduct',
      vus: 50,
      duration: '30m',
    },
    generate_report: {
      executor: 'constant-vus',
      exec: 'generateReport',
      vus: 50,
      duration: '30m',
    },
    consult_stock: {
      executor: 'constant-vus',
      exec: 'consultStock',
      vus: 50,
      duration: '30m',
    },
  },
};

// Basic auth credentials
const credentials = encoding.b64encode('super_caisse_user:supersecret');
const authHeaders = {
  headers: {
    Authorization: `Basic ${credentials}`,
    'Content-Type': 'application/json',
  },
};
const getHeaders = {
  headers: {
    Authorization: `Basic ${credentials}`,
  },
};

// Scenario: Mise à jour d'un produit
export function updateProduct() {
  const produitId = 1;
  const url = `http://localhost:5000/api/produits/${produitId}/`;
  const payload = JSON.stringify({
    nom: 'Produit Modifié K6',
    prix: 15.99,
    description: 'Mise à jour via K6',
  });
  const res = http.put(url, payload, authHeaders);
  check(res, {
    'status is 200': (r) => r.status === 200,
    'nom mis à jour': (r) => r.status === 200 && r.json('nom') === 'Produit Modifié K6',
    'prix mis à jour': (r) => r.status === 200 && parseFloat(r.json('prix')) === 15.99,
    'description mise à jour': (r) => r.status === 200 && r.json('description') === 'Mise à jour via K6',
  });
  sleep(0.05);
}

// Scenario: Génération de rapport consolidé
export function generateReport() {
  const magasinId = 7;
  const url = `http://localhost:5000/api/maison_mere/${magasinId}/tableau_de_bord/`;
  const res = http.get(url, getHeaders);
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

// Scenario: Consultation des stocks
export function consultStock() {
  const magasins = [1, 2, 3];
  magasins.forEach((id) => {
    const url = `http://localhost:5000/api/stocks/?magasin_id=${id}`;
    const res = http.get(url, getHeaders);
    let body = null;
    if (res.status === 200) {
      try {
        body = res.json();
      } catch {
        body = null;
      }
    }
    check(res, {
      [`stock status is 200 for store ${id}`]: (r) => r.status === 200,
      [`stock is array for store ${id}`]: () => Array.isArray(body),
    });
  });
  sleep(0.05);
}

// Default no-op function to satisfy k6
export default function () {
  // no operation
}
