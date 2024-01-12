URLS = {
    'auth': {
        'login': '/auth/login',
        'info': '/auth/info',
    },
    'posts': {
        'create': '/posts/create',
        'read': '/posts/{post_id}',
        'update': '/posts/{post_id}',
        'delete': '/posts/{post_id}',
    },
    'comments': {
        'create': '/comments/{post_id}/create_comments',
        'read': '/comments/{post_id}',
        'update': '/comments/{comment_id}',
        'delete': '/comments/{comment_id}',
    },
}


# Добавить URLs
# В первом примере определяется словарь URLS, который содержит
# набор URL-адресов для различных эндпоинтов в приложении.
# В данном случае определены адреса для эндпоинтов авторизации
# и изменения размера файлов.
