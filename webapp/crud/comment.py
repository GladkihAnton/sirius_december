# crud for comment

from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.models.sirius.comment import Comment


async def create_comment(session: AsyncSession, content: str, author_id: int, post_id: int) -> Comment:
    new_comment = Comment(content=content, author_id=author_id, post_id=post_id)
    session.add(new_comment)
    await session.commit()
    await session.refresh(new_comment)
    return new_comment


async def get_comment_by_id(session: AsyncSession, comment_id: int) -> Comment | None:
    result = await session.scalars(select(Comment).where(Comment.id == comment_id))
    return result.one_or_none()


async def update_comment(session: AsyncSession, comment_id: int, new_content: str) -> Comment | None:
    comment = await get_comment_by_id(session, comment_id)
    if comment:
        comment.content = new_content
        await session.commit()
        await session.refresh(comment)
        return comment
    return None


async def delete_comment(session: AsyncSession, comment_id: int) -> bool:
    comment = await get_comment_by_id(session, comment_id)
    if comment:
        await session.delete(comment)
        await session.commit()
        return True
    return False


async def get_comments_by_post(session: AsyncSession, post_id: int) -> List[Comment]:
    result = await session.scalars(select(Comment).where(Comment.post_id == post_id))
    return list(result.all())
