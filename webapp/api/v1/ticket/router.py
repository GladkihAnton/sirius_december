from webapp.models.sirius.ticket import Ticket
from webapp.schema.sirius.ticket import TicketDTO, TicketResponse
from webapp.utils.router.generate_crud import create_crud_routes

ticket_router = create_crud_routes(TicketDTO, TicketResponse, Ticket, "/ticket", tags=["ticket"])
