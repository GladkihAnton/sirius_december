from prometheus_client import Counter

get_patients_counter = Counter(
    'get_all_patients_responses',
    'Requests of all patients'
)
