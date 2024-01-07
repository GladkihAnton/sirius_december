# функционал для работы с постами (просмотр всех постов, просмотр одного поста по id, 
# удаление, редактирование (только тот пользователь что создал), 
# создание постов (только авторизованные пользователи)

from typing import List

import orjson
from fastapi import Depends, HTTPException, status
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from .router import post_router
from webapp.crud.post import create_post, delete_post, get_all_posts, get_post_by_id, get_posts_by_user, update_post
from webapp.db.postgres import get_session
from webapp.on_startup import redis as redis_startup
from webapp.schema.content.post import PostCreate, PostRead, PostUpdate
from webapp.schema.login.user import User
from webapp.utils.auth.user import get_current_user


# Дополнительная функция для инвалидации кэша
async def invalidate_cache_post(post_id: int):
    cache_key = f'posts_{post_id}'
    await redis_startup.redis.delete(cache_key) if redis_startup.redis is not None else None


@post_router.get('/', response_model=List[PostRead], response_class=ORJSONResponse, tags=['Posts'])
async def read_posts(session: AsyncSession = Depends(get_session)):
    cache_key = 'all_posts'
    cached_posts = await redis_startup.redis.get(cache_key) if redis_startup.redis is not None else None
    if cached_posts:
        # Десериализация кэшированных данных
        return [PostRead(**post) for post in orjson.loads(cached_posts)]

    posts = await get_all_posts(session)
    # Преобразование в модели Pydantic и сериализация
    pydantic_posts = [PostRead.from_orm(post) for post in posts]
    serialized_posts = orjson.dumps([post.dict() for post in pydantic_posts])
    await redis_startup.redis.set(cache_key, serialized_posts, ex=60) if redis_startup.redis is not None else None
    # Кэширование на 60 секунд
    return pydantic_posts


@post_router.get('/{post_id}', response_model=PostRead, response_class=ORJSONResponse, tags=['Posts'])
async def read_post_by_id(post_id: int, session: AsyncSession = Depends(get_session)):
    cache_key = f'posts_{post_id}'
    cached_post = await redis_startup.redis.get(cache_key) if redis_startup.redis is not None else None
    if cached_post:
        return PostRead.parse_raw(cached_post)

    post = await get_post_by_id(session, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')

    serialized_post = PostRead.from_orm(post).json()
    await redis_startup.redis.set(cache_key, serialized_post, ex=60) if redis_startup.redis is not None else None
    return PostRead.from_orm(post)


@post_router.get('/user/{user_id}', response_model=List[PostRead], response_class=ORJSONResponse, tags=['Posts'])
async def read_posts_by_user(user_id: int, session: AsyncSession = Depends(get_session)):
    posts = await get_posts_by_user(session, user_id)
    return [PostRead.from_orm(post) for post in posts]

#создание постов (только авторизованные пользователи)
@post_router.post( 
    '/create',
    response_model=PostRead,
    status_code=status.HTTP_201_CREATED,
    response_class=ORJSONResponse,
    tags=['Posts'],
)
async def create(
    post: PostCreate, session: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user) #current_user
):
    new_post = await create_post(session, post.content, current_user.id)
    return PostRead.from_orm(new_post)

# редактирование (только тот пользователь что создал)
@post_router.put('/{post_id}', response_model=PostRead, response_class=ORJSONResponse, tags=['Posts'])
async def update(
    post_id: int,
    post_update: PostUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    post = await get_post_by_id(session, post_id)
    if not post or post.author_id != current_user.id: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to update this post')
    if post_update.content and post_update.content is not None:
        updated_post = await update_post(session, post_id, post_update.content)
        await invalidate_cache_post(post_id)
        return PostRead.from_orm(updated_post)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Поле content не может быть пустым')


@post_router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT, response_class=ORJSONResponse, tags=['Posts'])
async def delete(
    post_id: int, session: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)
):
    post = await get_post_by_id(session, post_id)
    if not post or post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to delete this post')

    await delete_post(session, post_id)
    await invalidate_cache_post(post_id)
    return {'detail': 'Post deleted'}
