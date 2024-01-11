from webapp.api.patient.router import patient_router
from sqlalchemy.ext.asyncio import AsyncSession
from webapp.db.postgres import get_session
from fastapi import Depends, HTTPException
from webapp.crud.patient import delete_user
from starlette import status
from fastapi.responses import Response


@patient_router.delete('/{id:int}')
async def delete_user(id: int, session: AsyncSession = Depends(get_session)) -> Response:
    try:
        delete_user(id, session)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
