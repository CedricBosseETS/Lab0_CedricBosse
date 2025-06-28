import http from 'k6/http';
import { check } from 'k6';
import encoding from 'k6/encoding';

export default function () {
  const username = "super_caisse_user";
  const password = "supersecret";
  const credentials = `${username}:${password}`;
  const encodedCredentials = encoding.b64encode(credentials);
  const res = http.get("http://localhost:5000/api/magasins/", {
    headers: {
      Authorization: `Basic ${encodedCredentials}`,
    },
  });

  console.log(`Status code: ${res.status}`);

  check(res, {
    "status is 200": (r) => r.status === 200,
  });
}
