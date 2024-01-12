import orjson
from fastapi import Depends, HTTPException, status
from fastapi.responses import ORJSONResponse
from redis.exceptions import RedisError
from sqlalchemy.ext.asyncio import AsyncSession

from .router import post_router
from webapp import kafka_producer_decorator
from webapp.crud.post import (
    create_post,
    delete_post,
    get_all_posts,
    get_post_by_id,
    get_posts_by_user,
    update_post,
)
from webapp.db.postgres import get_session
from webapp.on_startup import redis as redis_startup
from webapp.schema.content.post import PostCreate, PostRead, PostUpdate
from webapp.schema.login.user import User
from webapp.utils.auth.user import get_current_user

CACHE_PREFIX_POST = 'post_'


# Дополнительная функция для инвалидации кэша
async def invalidate_cache_post(post_id: int):
    cache_key = f'{CACHE_PREFIX_POST}{post_id}'
    await redis_startup.redis.delete(
        cache_key
    ) if redis_startup.redis is not None else None


@post_router.get('/', tags=['Posts'])
@kafka_producer_decorator('get_post')
async def read_posts(
    session: AsyncSession = Depends(get_session),
    page: int = 1,
    per_page: int = 10,
):
    cache_key = f'{CACHE_PREFIX_POST}_all_{page}_{per_page}'
    try:
        cached_posts = await redis_startup.redis.get(cache_key)
        if cached_posts:
            cached_posts_data = orjson.loads(cached_posts)
            return ORJSONResponse(content=cached_posts_data)
    except RedisError as e:
        print(f'Ошибка Redis: {e}')

    posts, total_posts = await get_all_posts(session, page, per_page)
    pydantic_posts = [PostRead.model_validate(post) for post in posts]
    response_data = {
        'posts': [post.dict() for post in pydantic_posts],  # Изменено здесь
        'total_posts': total_posts,
    }
    try:
        await redis_startup.redis.set(
            cache_key, orjson.dumps(response_data), ex=60
        )
    except RedisError as e:
        print(f'Ошибка Redis: {e}')
    return ORJSONResponse(content=response_data)


@post_router.get(
    '/{post_id}',
    response_model=PostRead,
    response_class=ORJSONResponse,
    tags=['Posts'],
)
@kafka_producer_decorator('get_post')
async def read_post_by_id(
    post_id: int, session: AsyncSession = Depends(get_session)
):
    cache_key = f'{CACHE_PREFIX_POST}{post_id}'

    try:
        cached_post = await redis_startup.redis.get(cache_key)
        if cached_post:
            return PostRead.parse_raw(cached_post)
    except RedisError as e:
        print(f'Ошибка Redis: {e}')

    post = await get_post_by_id(session, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Post not found'
        )
    serialized_post = PostRead.model_validate(post).model_dump_json()

    try:
        await redis_startup.redis.set(cache_key, serialized_post, ex=60)
    except RedisError as e:
        print(f'Ошибка Redis: {e}')

    return PostRead.model_validate(post)


@post_router.get('/user/{user_id}', tags=['Posts'])
@kafka_producer_decorator('get_post')
async def read_posts_by_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    page: int = 1,
    per_page: int = 10,
):
    cache_key = f'{CACHE_PREFIX_POST}_user_{user_id}_{page}_{per_page}'

    try:
        cached_posts = await redis_startup.redis.get(cache_key)
        if cached_posts:
            return ORJSONResponse(content=orjson.loads(cached_posts))
    except RedisError as e:
        print(f'Ошибка Redis: {e}')

    posts, total = await get_posts_by_user(session, user_id, page, per_page)
    pydantic_posts = [PostRead.model_validate(post) for post in posts]
    response_data = {
        'posts': [post.dict() for post in pydantic_posts],
        'total_posts': total,
    }

    try:
        await redis_startup.redis.set(
            cache_key, orjson.dumps(response_data), ex=60
        )
    except RedisError as e:
        print(f'Ошибка Redis: {e}')

    return ORJSONResponse(content=response_data)


@post_router.post(
    '/create',
    response_model=PostRead,
    status_code=status.HTTP_201_CREATED,
    response_class=ORJSONResponse,
    tags=['Posts'],
)
@kafka_producer_decorator('create_post', status.HTTP_201_CREATED)
async def create(
    post: PostCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    new_post = await create_post(session, post.content, current_user.id)
    return PostRead.model_validate(new_post)


@post_router.put(
    '/{post_id}',
    response_model=PostRead,
    response_class=ORJSONResponse,
    tags=['Posts'],
)
@kafka_producer_decorator('update_post')
async def update(
    post_id: int,
    post_update: PostUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    post = await get_post_by_id(session, post_id)
    if not post or post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not authorized to update this post',
        )
    if post_update.content and post_update.content is not None:
        updated_post = await update_post(session, post_id, post_update.content)
        await invalidate_cache_post(post_id)
        return PostRead.model_validate(updated_post)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Поле content не может быть пустым',
        )


@post_router.delete(
    '/{post_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=ORJSONResponse,
    tags=['Posts'],
)
@kafka_producer_decorator('delete_post', status.HTTP_204_NO_CONTENT)
async def delete(
    post_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    post = await get_post_by_id(session, post_id)
    if not post or post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not authorized to delete this post',
        )

    await delete_post(session, post_id)
    await invalidate_cache_post(post_id)
    return {'detail': 'Post deleted'}
