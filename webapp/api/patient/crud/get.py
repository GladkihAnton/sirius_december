from webapp.api.patient.router import patient_router
from webapp.models.clinic.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from webapp.db.postgres import get_session
from sqlalchemy import select
from typing import List, Any
from fastapi.responses import ORJSONResponse
from webapp.pydantic_schemas.user import UserModel
from webapp.metrics import resp_counter, errors_counter
from fastapi import Depends, HTTPException
from starlette import status


@patient_router.get('/all', response_model=List[UserModel])
async def get_patients(session: AsyncSession = Depends(get_session)) -> ORJSONResponse:
    resp_counter.labels(endpoint='GET /patient/all').inc()
    users = (await session.execute(select(User))).scalars()
    users_json = [UserModel.model_validate(user).model_dump(mode='json') for user in users]
    return ORJSONResponse(users_json)


@patient_router.get('/{id:int}', response_model=UserModel)
async def get_patient(id: int, session: AsyncSession = Depends(get_session)) -> dict[str, Any]:
    resp_counter.labels(endpoint='GET /patient').inc()
    try:
        select_resp = select(User).where(User.id == id)
        patient_elem = (await session.scalars(select_resp)).one()
        return UserModel.model_validate(patient_elem).model_dump(mode='json')
    except Exception:
        errors_counter.labels(endpoint='GET /patient').inc()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
