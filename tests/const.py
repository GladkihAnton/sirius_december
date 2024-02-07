from typing import Any, Dict

from webapp.api.crud.const import API_PREFIX

URLS: Dict[str, Any] = {
    'auth': {
        'login': '/auth/login',
        'info': '/auth/info',
    },
    'client': {
        'resize': '/api/v1/client',
    },
}