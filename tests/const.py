URLS = {
    'auth': {
        'login': '/auth/login',
        'info': '/auth/info',
    },
    'user': {
        'create_user': '/users/signup',
        'get_del_user_by_id': '/users/{user_id}',
        'get_me': '/users/me',
        'get_my_subscriptions': '/users/me/subscriptions',
    },
    'course': {
        'get_post_courses': '/courses',
        'get_put_del_course_by_id': '/courses/{course_id}',
        'get_subscribers': '/courses/{course_id}/subscribers',
        'subscribe_to_course': '/courses/{course_id}/subscribe',
    },
    'lesson': {
        'get_post_lessons': '/courses/{course_id}/lessons',
        'get_put_del_lesson_by_id': '/courses/{course_id}/lessons/{lesson_id}',
    },
    'file': {
        'upload': '/courses/{course_id}/lessons/{lesson_id}/upload',
        'all_files_by_lesson': '/courses/{course_id}/lessons/{lesson_id}/files',
        'get_del_file_by_id': '/courses/{course_id}/lessons/{lesson_id}/files/{file_id}',
    },
}
