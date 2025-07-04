import http from 'k6/http';
import { check, sleep } from 'k6';
import encoding from 'k6/encoding';

export let options = {
  vus: 100,
  duration: '60s',
};

export default function () {
  const credentials = encoding.b64encode("super_caisse_user:supersecret");
  const headers = { Authorization: `Basic ${credentials}` };

  const magasins = [1, 2, 3];
  magasins.forEach((id) => {
    const url = `http://localhost:5000/api/stocks/?magasin_id=${id}`;
    const res = http.get(url, { headers });

    // Ne parser le JSON qu'en cas de 200
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
