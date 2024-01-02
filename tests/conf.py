from typing import Any, Dict

from webapp.api.crud.const import API_PREFIX

URLS: Dict[str, Any] = {
    'auth': {
        'login': '/auth/login',
        'info': '/auth/info',
        'register': '/auth/register',
    },
    'crud': {
        'activity': {
            'create': f'{API_PREFIX}/activity/create/',
            'read': f'{API_PREFIX}/activity/',
            'update': f'{API_PREFIX}/activity/update/',
            'delete': f'{API_PREFIX}/activity/delete/',
        },
        'reservation': {
            'create': f'{API_PREFIX}/reservation/create/',
            'read': f'{API_PREFIX}/reservation/',
            'update': f'{API_PREFIX}/reservation/update/',
            'delete': f'{API_PREFIX}/reservation/delete/',
        },
        'review': {
            'create': f'{API_PREFIX}/review/create/',
            'read': f'{API_PREFIX}/review/',
            'update': f'{API_PREFIX}/review/update/',
            'delete': f'{API_PREFIX}/review/delete/',
        },
        'tour': {
            'create': f'{API_PREFIX}/tour/create/',
            'read': f'{API_PREFIX}/tour/',
            'update': f'{API_PREFIX}/tour/update/',
            'delete': f'{API_PREFIX}/tour/delete/',
        },
        'user': {
            'read': f'{API_PREFIX}/user/',
            'update': f'{API_PREFIX}/user/update/',
            'delete': f'{API_PREFIX}/user/delete/',
        },
    },
}
