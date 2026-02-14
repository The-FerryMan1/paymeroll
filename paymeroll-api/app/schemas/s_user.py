from pydantic import BaseModel, ConfigDict, EmailStr, EmailStr
# username: Mapped[str] = mapped_column(String(255), index=True, unique=True)
#     full_name: Mapped[str] = mapped_column(String(255))
#     email: Mapped[str] = mapped_column(String(255), unique=True)
#     contact_no: Mapped[str] = mapped_column()

class UserBase(BaseModel):
    username: str
    full_name: str
    email: EmailStr
    contact_no: str

class UserCreate(UserBase):
    password: str

class UserResponsePublic(BaseModel):
    id: int
    username: str

class UserResponsePrivate(UserResponsePublic):
    full_name: str
    email: EmailStr
    contact_no: str
    role: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True) 

class UserUpdate(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None
    contact_no: str | None = None
    password: str | None = None
    role: str | None = None
    is_active: bool | None = None

class Token(BaseModel):
    access_token: str
    token_type: str

class UserLogin(BaseModel):
    username: str
    password: str

