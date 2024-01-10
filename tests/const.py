URLS = {
    'auth': {
        'login': '/auth/login',
        'info': '/auth/info',
    },
    'file': {
        'resize': '/file/resize',
    },
    'posts': {
        'create': '/posts/create',
        'read': '/posts',
        'update': '/posts/{post_id}',
        'delete': '/posts/{post_id}',
    },
}


# Добавить URLs
# В первом примере определяется словарь URLS, который содержит набор URL-адресов для различных эндпоинтов в приложении. В данном случае определены адреса для эндпоинтов авторизации и изменения размера файлов.