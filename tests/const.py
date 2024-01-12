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
            "ingredient": 
                {
                    "ingredient": API_PREFIX + "/ingredient"
                },
            "recipe": 
                {
                    "recipe": API_PREFIX + "/recipe"
                },
        }
}