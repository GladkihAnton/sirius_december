from typing import Any, Dict

from webapp.api.crud.const import API_PREFIX

URLS: Dict[str, Any] = {
    'auth': {
        'login': '/auth/login',
        'info': '/auth/info',
        'register': '/auth/register',
    },
    'crud': {
        'restaurant': {
            'create': f'{API_PREFIX}/restaurant/create',
            'read': f'{API_PREFIX}/restaurant/',
            'page': f'{API_PREFIX}/restaurant/page/',
            'update': f'{API_PREFIX}/restaurant/update/',
            'delete': f'{API_PREFIX}/restaurant/delete/',
        },
        'order': {
            'create': f'{API_PREFIX}/order/create',
            'read': f'{API_PREFIX}/order/',
            'page': f'{API_PREFIX}/order/page/',
            'update': f'{API_PREFIX}/order/update/',
            'delete': f'{API_PREFIX}/order/delete/',
        },
        'order_product': {
            'create': f'{API_PREFIX}/order_product/create',
            'read': f'{API_PREFIX}/order_product/',
            'page': f'{API_PREFIX}/order_product/page/',
            'update': f'{API_PREFIX}/order_product/update/',
            'delete': f'{API_PREFIX}/order_product/delete/',
        },
        'product': {
            'create': f'{API_PREFIX}/product/create',
            'read': f'{API_PREFIX}/product/',
            'page': f'{API_PREFIX}/product/page/',
            'update': f'{API_PREFIX}/product/update/',
            'delete': f'{API_PREFIX}/product/delete/',
        },
        'user': {
            'create': f'{API_PREFIX}/user/create',
            'read': f'{API_PREFIX}/user/',
            'page': f'{API_PREFIX}/user/page/',
            'update': f'{API_PREFIX}/user/update/',
            'delete': f'{API_PREFIX}/user/delete/',
        },
    },
}
