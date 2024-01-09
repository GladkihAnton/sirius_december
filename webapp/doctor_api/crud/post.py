from webapp.doctor_api.router import doctor_router
from webapp.models.clinic.doctor import Doctor
from sqlalchemy.ext.asyncio import AsyncSession
from webapp.db.postgres import get_session
from sqlalchemy import insert
from fastapi import Depends
from webapp.pydantic_schemas.doctor import DoctorCreateModel
from fastapi.responses import ORJSONResponse
from webapp.metrics import resp_counter
from starlette import status


@doctor_router.post('/')
async def create_doctor(body: DoctorCreateModel, session: AsyncSession = Depends(get_session)) -> ORJSONResponse:
    resp_counter.labels(endpoint='POST /doctor/').inc()
    new_id = (
        await session.scalars(
            insert(Doctor).values(
                {
                    'last_name': body.last_name,
                    'first_name': body.first_name,
                    'specialization': body.specialization,
                },
            ).returning(Doctor.id),
        )
    ).one()
    await session.commit()
    return ORJSONResponse(
        content={'id': new_id},
        status_code=status.HTTP_201_CREATED,
    )
