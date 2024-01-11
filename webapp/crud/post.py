from typing import List, Tuple

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.models.sirius.post import Post


async def get_all_posts(
    session: AsyncSession, page: int, per_page: int
) -> Tuple[List[Post], int]:
    offset = (page - 1) * per_page
    result = await session.scalars(select(Post).limit(per_page).offset(offset))
    posts = list(result.all())
    total_posts = await session.scalar(select(func.count(Post.id)))
    return posts, total_posts


async def create_post(
    session: AsyncSession, content: str, author_id: int
) -> Post:
    new_post = Post(content=content, author_id=author_id)
    session.add(new_post)
    await session.commit()
    await session.refresh(new_post)
    return new_post


async def get_post_by_id(session: AsyncSession, post_id: int) -> Post | None:
    result = await session.scalars(select(Post).where(Post.id == post_id))
    return result.one_or_none()


async def update_post(
    session: AsyncSession, post_id: int, new_content: str
) -> Post | None:
    post = await get_post_by_id(session, post_id)
    if post:
        post.content = new_content
        await session.commit()
        await session.refresh(post)
    return post


async def delete_post(session: AsyncSession, post_id: int) -> bool:
    post = await get_post_by_id(session, post_id)
    if post:
        await session.delete(post)
        await session.commit()
        return True
    return False


async def get_posts_by_user(
    session: AsyncSession, user_id: int, page: int, per_page: int
) -> Tuple[List[Post], int]:
    offset = (page - 1) * per_page
    result = await session.scalars(
        select(Post)
        .where(Post.author_id == user_id)
        .limit(per_page)
        .offset(offset)
    )
    posts = list(result.all())
    total_posts = await session.scalar(
        select(func.count()).where(Post.author_id == user_id).select_from(Post)
    )
    return posts, total_posts