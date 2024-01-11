from fastapi import APIRouter

from webapp.api.crud.const import API_PREFIX

v1_router = APIRouter(prefix=f'{API_PREFIX}/v1')
