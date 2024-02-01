from fastapi import APIRouter

from webapp.api.crud.const import API_PREFIX

activity_router = APIRouter(prefix=f'{API_PREFIX}/activity', tags=['Activity'])
