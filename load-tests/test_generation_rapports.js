import http from 'k6/http';
import { check,sleep } from 'k6';
import encoding from 'k6/encoding';

export let options = {
    vus: 5,
    duration: '20s',
};

export default function () {
    const magasinId = 7;
    const url = `http://localhost:5000/api/maison_mere/${magasinId}/rapport_ventes/`;
    const credentials = encoding.b64encode("super_caisse_user:supersecret");
    const res = http.get(url, {
        headers: {
            Authorization: `Basic ${credentials}`,
        },
    });

    check(res, {
        'status is 200': (r) => r.status === 200,
    });

    sleep(1);
}

