from fastapi import APIRouter

from webapp.api.crud.const import API_PREFIX

restaurant_router = APIRouter(prefix=f'{API_PREFIX}/restaurant')
