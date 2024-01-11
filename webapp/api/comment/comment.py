import orjson
from fastapi import Depends, HTTPException, status
from fastapi.responses import ORJSONResponse
from redis.exceptions import RedisError
from sqlalchemy.ext.asyncio import AsyncSession

from .router import comment_router
from webapp import kafka_producer_decorator
from webapp.crud.comment import (
    create_comment,
    delete_comment,
    get_comment_by_id,
    get_comments_by_post,
    update_comment,
)
from webapp.db.postgres import get_session
from webapp.models.sirius.user import User
from webapp.on_startup import redis as redis_startup
from webapp.schema.content.comment import (
    CommentCreate,
    CommentRead,
    CommentUpdate,
)
from webapp.utils.auth.user import get_current_user

CACHE_PREFIX_COMMENT = 'comment_'


# Дополнительная функция для инвалидации кэша
async def invalidate_cache(post_id: int):
    cache_key = f'{CACHE_PREFIX_COMMENT}{post_id}'
    await redis_startup.redis.delete(
        cache_key
    ) if redis_startup.redis is not None else None


@comment_router.get('/{post_id}', tags=['Comments'])
@kafka_producer_decorator('get_comments')
async def read_comments(
    post_id: int,
    session: AsyncSession = Depends(get_session),
    page: int = 1,
    per_page: int = 5,
):
    cache_key = f'{CACHE_PREFIX_COMMENT}{post_id}_{page}_{per_page}'

    try:
        cached_comments = await redis_startup.redis.get(cache_key)
        if cached_comments:
            return ORJSONResponse(content=orjson.loads(cached_comments))
    except RedisError as e:
        # Обработка ошибки подключения к Redis
        print(f'Redis error: {e}')

    comments, total_comments = await get_comments_by_post(
        session, post_id, page, per_page
    )
    pydantic_comments = [
        CommentRead.model_validate(comment.__dict__) for comment in comments
    ]
    response_data = {
        'comments': [comment.dict() for comment in pydantic_comments],
        'total_comments': total_comments,
    }
    serialized_comments = orjson.dumps(response_data)

    try:
        await redis_startup.redis.set(cache_key, serialized_comments, ex=60)
    except RedisError as e:
        # Обработка ошибки записи в Redis
        print(f'Redis error: {e}')

    return ORJSONResponse(content=response_data)


@comment_router.post(
    '/{post_id}/create_comments',
    response_model=CommentRead,
    status_code=status.HTTP_201_CREATED,
    response_class=ORJSONResponse,
    tags=['Comments'],
)
@kafka_producer_decorator('create_comments')
async def create(
    post_id: int,
    comment: CommentCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    created_comment = await create_comment(
        session, comment.content, current_user.id, post_id
    )
    await invalidate_cache(post_id)
    return CommentRead.model_validate(created_comment)


@comment_router.put(
    '/{comment_id}',
    response_model=CommentRead,
    response_class=ORJSONResponse,
    tags=['Comments'],
)
@kafka_producer_decorator('update_comments')
async def update(
    comment_id: int,
    comment_update: CommentUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    comment = await get_comment_by_id(session, comment_id)
    if not comment or comment.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not authorized to update this comment',
        )
    if comment_update.content and comment_update.content is not None:
        updated_comment = await update_comment(
            session, comment_id, comment_update.content
        )
        await invalidate_cache(comment.post_id)
        return CommentRead.model_validate(updated_comment)
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Поле content не может быть пустым',
    )


@comment_router.delete(
    '/{comment_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=ORJSONResponse,
    tags=['Comments'],
)
@kafka_producer_decorator('delete_comments')
async def delete(
    comment_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    comment = await get_comment_by_id(session, comment_id)
    if not comment or comment.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not authorized to delete this comment',
        )

    await delete_comment(session, comment_id)
    await invalidate_cache(comment.post_id)
    return {'detail': 'Comment deleted'}