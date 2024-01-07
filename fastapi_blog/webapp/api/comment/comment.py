# функционал для работы с комментариями (просмотр, создание, обновление, удаление)
from typing import List

import orjson
from fastapi import Depends, HTTPException, status
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from .router import comment_router
from webapp.crud.comment import create_comment, delete_comment, get_comment_by_id, get_comments_by_post, update_comment
from webapp.db.postgres import get_session
from webapp.models.sirius.user import User
from webapp.on_startup import redis as redis_startup
from webapp.schema.content.comment import CommentCreate, CommentRead, CommentUpdate
from webapp.utils.auth.user import get_current_user


# дополнительная функция для инвалидации кэша
# при обновлении или удалении поста мы могли удалить соответствующий кэш-ключ из Redis, чтобы при следующем запросе к этому посту данные были получены из базы данных, а не из устаревшего кэша
async def invalidate_cache(post_id: int):
    cache_key = f'comments_{post_id}'
    await redis_startup.redis.delete(cache_key) if redis_startup.redis is not None else None

# чтение комментариев
# при чтении комментариев происходит проверка наличия кэшированных данных в Redis. Если кэшированные данные есть, они десериализуются с помощью orjson и возвращаются в виде списка экземпляров 
@comment_router.get('/{post_id}', response_model=List[CommentRead], response_class=ORJSONResponse, tags=['Comments']) # сериализация и десериализация JSON в Python
async def read_comments(post_id: int, session: AsyncSession = Depends(get_session)):
    cache_key = f'comments_{post_id}'
    cached_comments = await redis_startup.redis.get(cache_key) if redis_startup.redis is not None else None
    if cached_comments:
        # десериализация кэшированных данных
        return [CommentRead(**comment) for comment in orjson.loads(cached_comments)]
    
    # если кэшированных данных нет, то данные получаются из базы данных и преобразуются в экземпляры модели Pydantic CommentRead
    comments = await get_comments_by_post(session, post_id)
    # преобразование в модели Pydantic и сериализация
    pydantic_comments = [CommentRead.from_orm(comment) for comment in comments]
    serialized_comments = orjson.dumps([comment.dict() for comment in pydantic_comments]) # данные сериализуются с помощью orjson и сохраняются в Redis на 60 секунд
    await redis_startup.redis.set(cache_key, serialized_comments, ex=60) if redis_startup.redis is not None else None
    return pydantic_comments #возвращается список экземпляров модели Pydantic CommentRead


@comment_router.post(
    '/{post_id}/create_comments',
    response_model=CommentRead,
    status_code=status.HTTP_201_CREATED,
    response_class=ORJSONResponse,
    tags=['Comments'],
)
async def create(
    post_id: int,
    comment: CommentCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    created_comment = await create_comment(session, comment.content, current_user.id, post_id)
    await invalidate_cache(post_id)
    return CommentRead.from_orm(created_comment)


@comment_router.put('/{comment_id}', response_model=CommentRead, response_class=ORJSONResponse, tags=['Comments'])
async def update(
    comment_id: int,
    comment_update: CommentUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    comment = await get_comment_by_id(session, comment_id)
    if not comment or comment.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to update this comment')
    if comment_update.content and comment_update.content is not None:
        updated_comment = await update_comment(session, comment_id, comment_update.content)
        await invalidate_cache(comment.post_id)
        return CommentRead.from_orm(updated_comment)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Поле content не может быть пустым')


@comment_router.delete(
    '/{comment_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=ORJSONResponse,
    tags=['Comments'],
)
async def delete(
    comment_id: int, session: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)
):
    comment = await get_comment_by_id(session, comment_id)
    if not comment or comment.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to delete this comment')

    await delete_comment(session, comment_id)
    await invalidate_cache(comment.post_id)
    return {'detail': 'Comment deleted'}

# кэширование - это процесс сохранения данных в памяти для быстрого доступа к ним в будущем. В данном случае, мы используем Redis как кэш-сервер, чтобы ускорить доступ к данным из базы данных. Кэширование позволяет уменьшить нагрузку на базу данных и сократить время отклика сервера.
# Pydantic - это библиотека для сериализации и десериализации данных. Она позволяет определять схемы данных в виде классов Python и автоматически преобразовывать данные в объекты этих классов и наоборот. Pydantic также обеспечивает проверку типов данных и валидацию входных данных.
# ORJSON - это библиотека для сериализации и десериализации JSON, написанная на языке C. Она быстрее стандартной библиотеки Python json и используется для оптимизации производительности при работе с большими объемами данных.