//api ne gere pas modifier produit... oups
import http from 'k6/http';
import { check, sleep } from 'k6';
import encoding from 'k6/encoding';

export let options = {
    vus: 5,
    duration: '20s',
};

export default function () {
    const produitId = 1; // à adapter si nécessaire
    const url = `http://localhost:5000/api/produits/${produitId}/`;
    const credentials = encoding.b64encode("super_caisse_user:supersecret");

    const payload = JSON.stringify({
        nom: "Produit Modifié",
        prix: 15.99,
        description: "Nouveau produit avec mise à jour via K6",
        categorie: "nouvelle_categorie"
    });

    const headers = {
        Authorization: `Basic ${credentials}`,
        'Content-Type': 'application/json',
    };

    const res = http.put(url, payload, { headers });

    check(res, {
        'status is 200 or 204': (r) => r.status === 200 || r.status === 204,
    });

    sleep(1);
}
