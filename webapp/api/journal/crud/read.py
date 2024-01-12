from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from starlette import status

from webapp.api.journal.router import journal_router
from webapp.db.postgres import get_session
from webapp.models.sirius.group import Group
from webapp.models.sirius.group_subject import GroupSubject
from webapp.models.sirius.journal import Journal
from webapp.models.sirius.student import Student
from webapp.models.sirius.subject import Subject
from webapp.schema.journal import StudentsJournal
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@journal_router.get('/student/{student_id}', response_model=StudentsJournal)
async def read_student_journal(
    student_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    # subjects_subquery = (
    #     select(
    #         Subject.id,
    #         Subject.title,
    #         func.jsonb_agg(
    #             func.jsonb_build_object(
    #                 'id', Journal.id,
    #                 'grade', Journal.grade,
    #                 'class_data', Journal.class_date
    #             )
    #         ).label('records')
    #     )
    #     .join(Journal, Subject.id == Journal.subject_id)
    #     .group_by(Subject.id)
    #     .alias()
    # )

    # query = (
    #     select(
    #         Student.id,
    #         Student.first_name,
    #         Student.last_name,
    #         Student.surname,
    #         Student.birthdate,
    #         func.jsonb_agg(
    #             func.jsonb_build_object(
    #                 'id', subjects_subquery.c.id,
    #                 'title', subjects_subquery.c.title,
    #                 'records', subjects_subquery.c.records
    #             )
    #         ).label('subjects')
    #     )
    #     .join(Group, Student.group_id == Group.id)
    #     .outerjoin(GroupSubject, Group.id == GroupSubject.group_id)
    #     .outerjoin(subjects_subquery, GroupSubject.subject_id == subjects_subquery.c.id)
    #     .filter(Student.id == student_id)
    #     .group_by(Student.id, Student.first_name, Student.last_name, Student.surname, Student.birthdate)
    # )

    query = (
        select(
            Student.id,
            Student.first_name,
            Student.last_name,
            Student.surname,
            Student.birthdate,
        )
        .join(Group)
        .join(GroupSubject)
        .join(Subject, GroupSubject.c.subject_id == Subject.id)
        .join(Journal, (Student.id == Journal.student_id) & (Subject.id == Journal.subject_id))
        .filter(Student.id == student_id)
        .options(selectinload(Student.records).selectinload(Journal.subject))
    )

    result = (await session.execute(query)).one_or_none()
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    students_journal_data = []
    current_student = None
    for row in result:
        if current_student is None or current_student['id'] != row['id']:
            if current_student is not None:
                students_journal_data.append(current_student)
            current_student = {
                'id': row['id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'surname': row['surname'],
                'birthdate': row['birthdate'],
                'subjects': [],
            }
        current_student['subjects'].append(
            {
                'id': row['subject_id'],
                'title': row['subject_title'],
                'records': [
                    {
                        'id': row['journal_id'],
                        'grade': row['grade'],
                        'class_date': row['class_date'],
                    }
                ],
            }
        )

    # Append the last student
    if current_student is not None:
        students_journal_data.append(current_student)

    json_result = StudentsJournal.model_validate(result).model_dump(mode='json')

    return ORJSONResponse(json_result)
