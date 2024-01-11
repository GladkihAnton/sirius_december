from webapp.models.sirius.event import Event
from webapp.schema.sirius.event import EventDTO, EventResponse
from webapp.utils.router.generate_crud import create_crud_routes

event_router = create_crud_routes(EventDTO, EventResponse, Event, "/event", tags=["event"])
