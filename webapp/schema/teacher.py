from typing import Optional

from pydantic import BaseModel, ConfigDict

from webapp.schema.user import UserRead


class TeacherBase(BaseModel):
    first_name: str
    last_name: str
    surname: Optional[str] = None


class TeacherInfo(TeacherBase):
    user_id: int
    institution_id: int


class TeacherRead(TeacherBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    institution_id: int
    user: UserRead
