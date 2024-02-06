import asyncio
from typing import List

from fastapi import UploadFile
from minio.error import S3Error
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.db.minio import minio_client
from webapp.models.sirius.file import File as SQLAFile
from webapp.models.sirius.lesson import Lesson as SQLALesson
from webapp.schema.file.file import FileCreate, FileRead


async def upload_file_to_minio(file: UploadFile, course_id: int, lesson_id: int) -> str:
    bucket_name = f'course-{course_id}-lesson-{lesson_id}'

    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)

    file_path = f'files/{file.filename}'
    file_size = file.file.tell()
    file.file.seek(0)

    await asyncio.get_event_loop().run_in_executor(
        None,
        minio_client.put_object,
        bucket_name,
        file_path,
        file.file,
        file_size,
        file.content_type,
    )

    return file_path


async def create_file(
    session: AsyncSession, file_data: FileCreate, file: UploadFile, course_id: int, lesson_id: int
) -> FileRead:
    minio_path = await upload_file_to_minio(file=file, course_id=course_id, lesson_id=lesson_id)
    new_file = SQLAFile(**file_data.model_dump(), minio_path=minio_path)
    session.add(new_file)
    await session.commit()
    await session.refresh(new_file)
    return FileRead.model_validate(new_file)


async def get_file_by_id(session: AsyncSession, file_id: int) -> FileRead | None:
    result = await session.execute(select(SQLAFile).where(SQLAFile.id == file_id))
    file = result.scalars().first()
    if file:
        return FileRead.model_validate(file)
    return None


async def delete_file(session: AsyncSession, course_id: int, lesson_id: int, file_id: int) -> bool:
    result = await session.execute(select(SQLAFile).where(SQLAFile.id == file_id))
    file = result.scalars().first()
    if file:
        try:
            minio_client.remove_object(f'course-{course_id}-lesson-{lesson_id}', file.minio_path)
            await session.delete(file)
            await session.commit()
            return True
        except S3Error:
            return False
    return False


async def get_files_by_lesson_id(
    session: AsyncSession, course_id: int, lesson_id: int, page: int = 1, page_size: int = 10
) -> List[FileRead] | None:
    result = await session.execute(
        select(SQLAFile)
        .join(SQLALesson, SQLALesson.id == SQLAFile.lesson_id)
        .where(SQLALesson.id == lesson_id, SQLALesson.course_id == course_id)
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    files = result.scalars().all()
    if files:
        return [FileRead.model_validate(file) for file in files]
    return None
