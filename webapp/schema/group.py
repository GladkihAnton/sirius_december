from typing import List

from pydantic import BaseModel, ConfigDict

from webapp.schema.student import StudentRead


class GroupInfo(BaseModel):
    title: str
    institution_id: int


class GroupStudents(GroupInfo):
    model_config = ConfigDict(from_attributes=True)

    id: int
    students: List[StudentRead]
