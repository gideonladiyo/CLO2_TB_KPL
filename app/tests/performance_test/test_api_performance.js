import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
    vus: 10, // 10 virtual users
    duration: '30s', // selama 30 detik
};

const BASE_URL_ITEM = 'http://40.79.241.106:5151/item';
const BASE_URL_ORDER = 'http://40.79.241.106:5151/order';

// Data dummy untuk POST dan PUT
const dummyItem = {
    name: 'TestItem',
    price: 9999,
    stock: 100
};

const dummyOrder = {
    items: [
        {
            item_id: "I93412",
            quantity: 1
        },
        {
            item_id: "I44514",
            quantity: 1
        }
    ]
}

export default function () {
    // 1. GET
    // GET all items
    let res_items = http.get(`${BASE_URL_ITEM}/`);
    check(res_items, {
        'GET all status is 200': (r) => r.status === 200,
    });

    // GET all orders
    let res_orders = http.get(`${BASE_URL_ORDER}/`);
    check(res_orders, {
        'GET all status is 200': (r) => r.status === 200
    });

    // 2. POST
    let res_post_item = http.post(`${BASE_URL_ITEM}/`, JSON.stringify(dummyItem), {
        headers: { 'Content-Type': 'application/json' },
    });

    let res_post_order = http.post(`${BASE_URL_ORDER}/`, JSON.stringify(dummyOrder), {
        headers: { 'Content-Type': 'application/json' },
    });

    check(res_post_item, {
        'POST status is 201': (r) => r.status === 201,
    });

    check(res_post_order, {
        'POST status is 201': (r) => r.status === 201,
    });

    // Extract ID dari item baru
    const newItem = res_post_item.json().data;
    const item_id = newItem?.item_id;

    // Extract ID dari order baru
    const newOrder = res_post_order.json().data;
    const order_id = newOrder?.id;

    // 3. PUT UPDATE
    if (item_id) {
        let updateData = {
            name: 'UpdatedItem',
            price: 8888,
            stock: 150
        };

        let res3 = http.put(`${BASE_URL_ITEM}/${item_id}`, JSON.stringify(updateData), {
            headers: { 'Content-Type': 'application/json' },
        });

        check(res3, {
            'PUT status is 200': (r) => r.status === 200,
        });

        // DELETE item
        let res4 = http.del(`${BASE_URL_ITEM}/${item_id}`);
        check(res4, {
            'DELETE status is 200': (r) => r.status === 200 || r.status === 204,
        });
    }

    // change order state
    if (order_id) {
        let res_pay = http.post(`${BASE_URL_ORDER}/${order_id}/pay`)

        check(res_pay, {
            'POST order to PAID 201': (r) => r.status === 201,
        });

        let res_ship = http.post(`${BASE_URL_ORDER}/${order_id}/ship`)

        check(res_ship, {
            'POST order to SHIPPED 201': (r) => r.status === 201,
        });

        let res_complete = http.post(`${BASE_URL_ORDER}/${order_id}/complete`)

        check(res_complete, {
            'POST order to DELIVERED 201': (r) => r.status === 201,
        });
    }

    sleep(1); // delay antar virtual user
}
