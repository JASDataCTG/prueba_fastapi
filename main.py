""" EJEMPLO DE CÓDIGO
DCFC Investigación
Jairo Acosta Solano """

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from bd.database import engine, Base
from routers.movie import routerMovie
from routers.users import login_user

app = FastAPI(
    title="BackEnd de muestra del Profe Jairo",
    description="API de prueba",
    version="1.0",
)

app.include_router(routerMovie)
app.include_router(login_user)

Base.metadata.create_all(bind=engine)











""" movies = [
    {
        "id": 1,
        "titulo": "El Padrino",
        "resumen": "Pelicula de mafiosos",
        "anio": "1972",
        "rating": 9.2,
        "categoria": "Crimen",
    }
] """



@app.get("/", tags=["Inicio"])
def read_root():
    return HTMLResponse("<h1>Página de Inicio</h1>")
