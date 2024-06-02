from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from user_jwt import createToken


login_user = APIRouter()


class User(BaseModel):
    email: str
    password: str


@login_user.post("/login", tags=["Usuario"])
def login(user: User):
    if user.email == "jacosol@msn.com" and user.password == "1234":
        token: str = createToken(user.model_dump())
        print(token)
        return JSONResponse(content=token)
