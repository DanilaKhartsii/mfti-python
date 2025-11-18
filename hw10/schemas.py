from pydantic import BaseModel


class StudentCreate(BaseModel):
    name: str
    faculty: str


class StudentUpdate(BaseModel):
    name: str | None = None
    faculty: str | None = None


class StudentResponse(BaseModel):
    id: int
    name: str
    faculty: str

    class Config:
        orm_mode = True
