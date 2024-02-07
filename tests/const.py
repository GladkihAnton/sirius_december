from conf.config import settings

API_PREFIX = settings.API_PREFIX

URLS = {
    "api": {
            "auth": 
                {
                    "register": API_PREFIX + "/auth/register",
                    "login": API_PREFIX + "/auth/login",
                },
            "user": 
                {
                    "user": API_PREFIX + "/user"
                },
            "item": 
                {
                    "item": API_PREFIX + "/item"
                },
            "exchange": 
                {
                    "exchange": API_PREFIX + "/exchange"
                },
        }
}