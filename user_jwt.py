import os
import jwt
from dotenv import load_dotenv, dotenv_values

load_dotenv()

API_KEY = os.getenv("CLAVE_SECRETA")
# config = dotenv_values(".env")


def createToken(data: dict):
    token: str = jwt.encode(payload=data, key="CLAVE_SECRETA", algorithm="HS256")
    return token


def validateToken(token: str) -> dict:
    data: dict = jwt.decode(token, key="CLAVE_SECRETA", algorithms=["HS256"])
    return data
