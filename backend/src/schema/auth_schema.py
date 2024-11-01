from pydantic import BaseModel


class UserInfo(BaseModel):
    id: int
    login_id: str
    user_name: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class LoginRequest(BaseModel):
    login_id: str
    password: str


class LoginResponse(BaseModel):
    token: TokenResponse
    user: UserInfo


class RegisterRequest(BaseModel):
    login_id: str
    password: str
    user_name: str
    planet_name: str


class RegisterResponse(BaseModel):
    token: TokenResponse
    user: UserInfo
    planet: str
