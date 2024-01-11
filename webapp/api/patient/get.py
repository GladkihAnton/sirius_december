from webapp.api.patient.router import patient_router
from webapp.models.clinic.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from webapp.db.postgres import get_session
from sqlalchemy import select
from typing import List, Any
from fastapi.responses import ORJSONResponse
from webapp.pydantic_schemas.user import UserModel
from webapp.crud.patient import get_users, get_user
from fastapi import Depends, HTTPException
from starlette import status


@patient_router.get('/page/{page_num}', response_model=List[UserModel])
async def get_patients(page_num: int, session: AsyncSession = Depends(get_session)) -> ORJSONResponse:
    users = await get_users(page_num, session)
    users_json = [UserModel.model_validate(user).model_dump(mode='json') for user in users]
    return ORJSONResponse(users_json)


@patient_router.get('/{id:int}', response_model=UserModel)
async def get_patient(id: int, session: AsyncSession = Depends(get_session)) -> dict[str, Any]:
    try:
        patient_elem = await get_user(id, session)
        return UserModel.model_validate(patient_elem).model_dump(mode='json')
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
