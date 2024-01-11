from fastapi import Depends, status
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.api.v1.auth.router import login_router
from webapp.crud.generate import create_item
from webapp.db.postgres import get_session
from webapp.models.sirius.user import User
from webapp.schema.sirius.user import UserDTO, UserResponse
from webapp.utils.exceptions import handle_domain_error


@login_router.post(
    path="/registration",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
@handle_domain_error
async def registration(
    payload: UserDTO,
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    new_item = await create_item(session, User, payload)
    return ORJSONResponse(
        UserResponse.model_validate(new_item, from_attributes=True).model_dump(mode="json"),
        status_code=status.HTTP_201_CREATED,
    )
