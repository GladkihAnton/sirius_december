from fastapi import APIRouter

from webapp.api.crud.const import API_PREFIX

op_router = APIRouter(prefix=f'{API_PREFIX}/order_product')
