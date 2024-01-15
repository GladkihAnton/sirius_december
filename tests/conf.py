from typing import Any, Dict

from webapp.api.crud.const import API_PREFIX

URLS: Dict[str, Any] = {
    'auth': {
        'token': '/auth/token',
        'info': '/auth/info',
        'register': '/auth/register',
    },
    'crud': {
        'activity': f'{API_PREFIX}/activity/',
        'reservation': f'{API_PREFIX}/reservation/',
        'review': f'{API_PREFIX}/review/',
        'tour': f'{API_PREFIX}/tour/',
        'user': f'{API_PREFIX}/user/',
    },
}
