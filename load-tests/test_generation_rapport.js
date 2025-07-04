import http from 'k6/http';
import { check, sleep } from 'k6';
import encoding from 'k6/encoding';

export const options = {
  vus: 100,
  duration: '60s',
};

export default function () {
  const credentials = encoding.b64encode('super_caisse_user:supersecret');
  const headers     = { Authorization: `Basic ${credentials}` };

  const magasinId = 7;
  const url = `http://localhost:5000/api/maison_mere/${magasinId}/tableau_de_bord/`;
  const res = http.get(url, { headers });

  // Ne parser le JSON que si status 200
  let body = {};
  if (res.status === 200) {
    try {
      body = res.json();
    } catch (e) {
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
