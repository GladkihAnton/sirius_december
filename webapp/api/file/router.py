from fastapi import APIRouter

file_router = APIRouter(prefix='/courses/{course_id}/lessons/{lesson_id}')
