from fastapi import APIRouter

from webapp.api.crud.const import API_PREFIX

product_router = APIRouter(prefix=f'{API_PREFIX}/product')