from fastapi import APIRouter

from webapp.api.crud.const import API_PREFIX

client_router = APIRouter(prefix=f'{API_PREFIX}/client')
