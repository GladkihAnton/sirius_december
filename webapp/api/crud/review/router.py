from fastapi import APIRouter

from webapp.api.crud.const import API_PREFIX

review_router = APIRouter(prefix=f'{API_PREFIX}/review')
