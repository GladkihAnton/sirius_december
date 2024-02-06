from fastapi import APIRouter

course_router = APIRouter(prefix='/courses')
lesson_router = APIRouter(prefix='/courses/{course_id}/lessons')
subscribe_router = APIRouter(prefix='/subscribes')
