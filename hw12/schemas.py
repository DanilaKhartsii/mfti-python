from pydantic import BaseModel


# ---------- User ----------

class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str
    is_read_only: bool = False


class UserLogin(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    is_read_only: bool

    class Config:
        orm_mode = True


class TokenResponse(BaseModel):
    token: str


# ---------- Student ----------

class StudentBase(BaseModel):
    name: str
    faculty: str
    course: int


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: str | None = None
    faculty: str | None = None
    course: int | None = None


class StudentResponse(StudentBase):
    id: int

    class Config:
        orm_mode = True
