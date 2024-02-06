from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.api.education.router import subscribe_router
from webapp.crud.subscribe import create_subscription, delete_subscription
from webapp.db.postgres import get_session
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


# С помощью данного функционала преподаватель или администратор может создать или удалить подписку
# на курс любому пользователю
@subscribe_router.post('/', status_code=status.HTTP_201_CREATED, tags=['Subscribe'])
async def create_subscription_endpoint(
    user_id: int,
    course_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
):
    if current_user['role'] not in ['admin', 'teacher']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав для выполнения операции')
    try:
        success = await create_subscription(session, user_id, course_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Не удалось создать подписку')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Ошибка сервера: {str(e)}')


@subscribe_router.delete('/', status_code=status.HTTP_204_NO_CONTENT, tags=['Subscribe'])
async def delete_subscription_endpoint(
    user_id: int,
    course_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
):
    if current_user['role'] not in ['admin', 'teacher']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав для выполнения операции')
    try:
        success = await delete_subscription(session, user_id, course_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Подписка не найдена')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Ошибка сервера: {str(e)}')
