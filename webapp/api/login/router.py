from fastapi import APIRouter

auth_router = APIRouter(prefix='/auth')
user_router = APIRouter(prefix='/users')
