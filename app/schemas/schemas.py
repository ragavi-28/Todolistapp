from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):

    username: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):

    username: str
    password: str


class TodoCreate(BaseModel):

    title: str
    description: str | None = None


class TodoResponse(BaseModel):

    id: int
    title: str
    description: str | None
    completed: bool

    class Config:
        from_attributes = True