URLS = {
    'auth': {
        'login': '/auth/login',
        'info': '/auth/info',
    },
    'employee': {
        'create': '/employees',
        'get_delete_patch': '/employees/{employee_id}',
        'get_vacations_for_employee': '/employees/{employee_id}/vacations',
    },
    'vacation': {
        'get_post': '/vacations',
        'pending': '/vacations/pending',
        'get_by_id_and_delete': '/vacations/{vacation_id}',
        'requests': '/vacations/vacation-requests',
        'approval': '/vacations/{vacation_id}/approval',
    },
}
