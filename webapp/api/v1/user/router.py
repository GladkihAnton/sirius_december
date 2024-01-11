from webapp.models.sirius.user import User as UserDB
from webapp.schema.sirius.user import UserDTO, UserResponse
from webapp.utils.router.generate_crud import create_crud_routes

user_router = create_crud_routes(UserDTO, UserResponse, UserDB, "/user", tags=["user"])
