from typing import List

from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.login.router import user_router
from webapp.crud.course import CourseRead, get_courses_subscription
from webapp.crud.user import create_user, delete_user, get_user_by_id, update_user
from webapp.db.postgres import get_session
from webapp.schema.login.user import UserCreate, UserRead
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


async def get_courses_by_user_subscription(
    user_id: int,
    session: AsyncSession,
    current_user: JwtTokenT,
):
    return await get_courses_subscription(session=session, user_id=user_id)


@user_router.post(
    '/signup',
    response_model=UserRead,
    tags=['Users'],
    response_class=ORJSONResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user_endpoint(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
):
    if current_user['role'] == 'admin':
        try:
            user = await create_user(session=session, user_data=user_data)
            return user
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        raise HTTPException(status_code=403, detail='Нет доступа для выполнения этой операции')


@user_router.put('/{user_id}', response_model=UserRead, tags=['Users'], response_class=ORJSONResponse)
async def update_user_endpoint(
    user_id: int,
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
):
    if current_user['user_id'] == user_id or current_user['role'] == 'admin':
        try:
            user = await update_user(session=session, user_id=user_id, user_data=user_data)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Пользователь не найден')
            return user
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Нет доступа для выполнения этой операции')


@user_router.get('/me', response_model=UserRead, tags=['Users'], response_class=ORJSONResponse)
async def get_me_endpoint(
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
):
    try:
        user = await get_user_by_id(session=session, user_id=current_user['user_id'])
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Пользователь не найден')
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@user_router.get('/{user_id}', response_model=UserRead, tags=['Users'], response_class=ORJSONResponse)
async def get_user_by_id_endpoint(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
):
    try:
        user = await get_user_by_id(session=session, user_id=user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Пользователь не найден')
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@user_router.get('/me/subscriptions/', response_model=List[CourseRead], tags=['Users'], response_class=ORJSONResponse)
async def get_courses_by_user_me_subscription(
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
):
    try:
        user_id = current_user['user_id']
        courses = await get_courses_by_user_subscription(user_id=user_id, session=session, current_user=current_user)
        if not courses:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Подписки не найдены')
        return courses
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@user_router.get(
    '/{user_id}/subscriptions/', response_model=List[CourseRead], tags=['Users'], response_class=ORJSONResponse
)
async def get_courses_by_user_id_subscription(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
):
    # Дополнительная проверка, если доступ разрешен только для собственных подписок или для администраторов
    if current_user['role'] != 'admin' and current_user['user_id'] != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Нет доступа к этой информации')
    try:
        courses = await get_courses_by_user_subscription(user_id=user_id, session=session, current_user=current_user)
        if not courses:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Подписки не найдены')
        return courses
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@user_router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Users'])
async def delete_user_endpoint(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
):
    if current_user['role'] != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Нет доступа для выполнения этой операции')
    try:
        success = await delete_user(session=session, user_id=user_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Пользователь не найден')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
