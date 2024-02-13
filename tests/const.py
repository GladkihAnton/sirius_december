from typing import Any, Dict

from webapp.api.crud.const import API_PREFIX

URLS: Dict[str, Any] = {
    'auth': {
        'login': '/auth/login',
        'info': '/auth/info',
    },
    'client': {
        'create': '/api/v1/client/create',
        'get': '/api/v1/client/{client_id}',
        'delete': '/api/v1/client/delete/{client_id}',
        'update': '/api/v1/client/update/{client_id}',
    },
    'deal':{
        'create': '/api/v1/deal/create',
        'delete': '/api/v1/deal/delete/{deal_id}',
        'get': '/api/v1/deal/{deal_id}',
        'update': '/api/v1/deal/update/{deal_id}'
    }
}