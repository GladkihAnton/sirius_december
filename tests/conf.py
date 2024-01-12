from typing import Any, Dict

URLS: Dict[str, Any] = {
    "auth": {
        "login": "/auth/login",
        "info": "/auth/info",
        "register": "/auth/register",
    },
    "crud": {
        "task": {
            "create": "task/create",
            "read": "task/info/",
            "update": "task/update/",
            "delete": "task/delete/",
        },
        "category": {
            "create": "category/create",
            "read": "category/info/",
            "delete": "category/delete/",
            "update": "category/update/",
        },
    },
}
