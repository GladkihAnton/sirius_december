from webapp.api.patient.router import patient_router
from sqlalchemy.ext.asyncio import AsyncSession
from webapp.db.postgres import get_session
from fastapi import Depends, HTTPException
from starlette import status
from fastapi.responses import Response
from webapp.crud.timetable import delete_timetable_point


@patient_router.delete('/appointment/{timetable_id:int}')
async def delete_appointment(timetable_id: int, session: AsyncSession = Depends(get_session)) -> Response:
    try:
        delete_timetable_point(timetable_id, session)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
