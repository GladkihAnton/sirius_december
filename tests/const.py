from conf.config import settings

API_PREFIX = settings.API_PREFIX + settings.API_V1_PREFIX

URLS = {
    "api": {
        "v1": {
            "auth": {
                "registration": API_PREFIX + "/auth/registration",
                "token": API_PREFIX + "/auth/token",
            },
            "user": {"user": API_PREFIX + "/user"},
            "event": {"event": API_PREFIX + "/event"},
            "ticket": {"ticket": API_PREFIX + "/ticket"},
        }
    }
}
