from webapp.api.doctor.router import doctor_router
from sqlalchemy.ext.asyncio import AsyncSession
from webapp.db.postgres import get_session
from fastapi import Depends
from webapp.pydantic_schemas.doctor import DoctorCreateModel
from webapp.crud.doctor import create_doctor
from fastapi.responses import ORJSONResponse
from starlette import status


@doctor_router.post('/')
async def create_doctor(body: DoctorCreateModel, session: AsyncSession = Depends(get_session)) -> ORJSONResponse:
    new_id = await create_doctor(body.last_name, body.first_name, body.specialization, session)
    return ORJSONResponse(
        content={'id': new_id},
        status_code=status.HTTP_201_CREATED,
    )
