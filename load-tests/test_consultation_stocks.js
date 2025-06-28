//la requeête pour voir les produits n,est pas API donc maybe changer cela
import http from 'k6/http';
import { check, sleep } from 'k6';
import encoding from 'k6/encoding';

export let options = {
    vus: 10,
    duration: '30s',
};

export default function () {
    const credentials = encoding.b64encode("super_caisse_user:supersecret");
    const headers = {
        Authorization: `Basic ${credentials}`,
    };

    const magasins = [1, 2, 3];
    magasins.forEach(id => {
        let res = http.get(`http://localhost:5000/api/magasins/${id}/stock`, { headers });
        check(res, { "stock status is 200": (r) => r.status === 200 });
    });

    sleep(1);
}
