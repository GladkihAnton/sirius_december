from webapp.api.patient.router import patient_router
from sqlalchemy.ext.asyncio import AsyncSession
from webapp.db.postgres import get_session
from fastapi import Depends, HTTPException
from starlette import status
from fastapi.responses import ORJSONResponse
from webapp.pydantic_schemas.user import UserModel
from webapp.crud.patient import update_user


@patient_router.put('/')
async def update_user_data(body: UserModel, session: AsyncSession = Depends(get_session)) -> ORJSONResponse:
    try:
        updated_data = update_user(body.id, body.username, body.first_name, body.last_name, session)
        return ORJSONResponse(
            {
                'username': updated_data.username,
                'first_name': updated_data.first_name,
                'last_name': updated_data.last_name,
            },
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='username is already used',
        )
