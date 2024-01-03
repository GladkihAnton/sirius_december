from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.models.sirius.post import Post


async def get_all_posts(session: AsyncSession) -> List[Post]:
    result = await session.scalars(select(Post))
    return list(result.all())


async def create_post(session: AsyncSession, content: str, author_id: int) -> Post:
    new_post = Post(content=content, author_id=author_id)
    session.add(new_post)
    await session.commit()
    await session.refresh(new_post)
    return new_post


async def get_post_by_id(session: AsyncSession, post_id: int) -> Post | None:
    result = await session.scalars(select(Post).where(Post.id == post_id))
    return result.one_or_none()


async def update_post(session: AsyncSession, post_id: int, new_content: str) -> Post | None:
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


async def get_posts_by_user(session: AsyncSession, user_id: int) -> List[Post]:
    result = await session.scalars(select(Post).where(Post.author_id == user_id))
    return list(result.all())
