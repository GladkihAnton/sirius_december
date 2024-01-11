from pydantic import BaseModel, ConfigDict


class DoctorModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    specialization: str
    first_name: str
    last_name: str


class DoctorServiceID(BaseModel):
    doctor_id: int
    service_id: int


class DoctorCreateModel(BaseModel):
    specialization: str
    first_name: str
    last_name: str
