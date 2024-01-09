from pydantic import BaseModel, ConfigDict

from webapp.schema.teacher import TeacherRead


class SubjectBase(BaseModel):
    title: str


class SubjectInfo(SubjectBase):
    institution_id: int
    teacher_id: int


class SubjectRead(SubjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    teacher: TeacherRead
