from pydantic import BaseModel


class GroupSubjectInfo(BaseModel):
    subject_id: int
    group_id: int
