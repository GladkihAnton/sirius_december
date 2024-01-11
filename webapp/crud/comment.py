from typing import List, Tuple

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.models.sirius.comment import Comment


async def create_comment(
    session: AsyncSession, content: str, author_id: int, post_id: int
) -> Comment:
    new_comment = Comment(
        content=content, author_id=author_id, post_id=post_id
    )
    session.add(new_comment)
    await session.commit()
    await session.refresh(new_comment)
    return new_comment


async def get_comment_by_id(
    session: AsyncSession, comment_id: int
) -> Comment | None:
    result = await session.scalars(
        select(Comment).where(Comment.id == comment_id)
    )
    return result.one_or_none()


async def update_comment(
    session: AsyncSession, comment_id: int, new_content: str
) -> Comment | None:
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


async def get_comments_by_post(
    session: AsyncSession, post_id: int, page: int, per_page: int
) -> Tuple[List[Comment], int]:
    offset = (page - 1) * per_page
    comments_query = (
        select(Comment)
        .where(Comment.post_id == post_id)
        .limit(per_page)
        .offset(offset)
    )
    total_query = select(func.count(Comment.id)).where(
        Comment.post_id == post_id
    )
    comments_result = await session.scalars(comments_query)
    total_result = await session.scalar(total_query)
    comments = list(comments_result.all())
    total_comments = total_result
    return comments, total_comments