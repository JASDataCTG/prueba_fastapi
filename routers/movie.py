from fastapi import Depends, APIRouter, HTTPException, Path, Query, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field
from bd.database import Session
from models.movie import Movie as ModelMovie
from user_jwt import validateToken


routerMovie = APIRouter()


class Movie(BaseModel):
    # id: Optional[int] = None
    titulo: str = Field(default="Título de la película", min_length=5, max_length=60)
    resumen: str = Field(default="Resumen", min_length=5, max_length=60)
    anio: int = Field(default=2023)
    rating: float = Field(ge=1, le=10)
    categoria: str = Field(default="Categoría", min_length=5, max_length=15)


class BearerJWT(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validateToken(auth.credentials)
        if data["email"] != "jacosol@msn.com":
            raise HTTPException(status_code=403, details="Credenciales incorrectas")


@routerMovie.get("/movies", tags=["Películas"], dependencies=[Depends(BearerJWT())])
def get_movies():
    db = Session()
    data = db.query(ModelMovie).all()
    return JSONResponse(content=jsonable_encoder(data))


@routerMovie.get("/movies/{id}", tags=["Películas"], status_code=200)
def get_movie(id: int = Path(ge=1, le=100)):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(
            status_code=404, content={"Mensaje": "Recurso no encontrado"}
        )
    return JSONResponse(status_code=200, content=jsonable_encoder(data))


@routerMovie.get("/movies/", tags=["Películas"], status_code=200)
def get_movies_by_category(categoria: str = Query(min_length=3, max_length=15)):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.categoria == categoria).all()
    if not data:
        return JSONResponse(
            status_code=404, content={"Mensaje": "Recurso no encontrado"}
        )
    return JSONResponse(status_code=200, content=jsonable_encoder(data))


@routerMovie.post("/movies", tags=["Películas"], status_code=201)
def create_movie(movie: Movie):
    db = Session()
    newMovie = ModelMovie(**movie.model_dump())
    db.add(newMovie)
    db.commit()
    # movies.append(movie)
    return JSONResponse(
        status_code=201,
        content={"mensaje": "Se ha creado una película", "movie": [movie.model_dump()]},
    )


@routerMovie.put("/movies/{id}", tags=["Películas"], status_code=200)
def update_movie(id: int, movie: Movie):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(
            status_code=404, content={"Mensaje": "No se encuentra el recurso"}
        )
    data.titulo = movie.titulo
    data.resumen = movie.resumen
    data.anio = movie.anio
    data.rating = movie.rating
    data.categoria = movie.categoria
    db.commit()
    return JSONResponse(content={"mensaje": "Se ha actualizado la película"})


@routerMovie.delete("/movies/{id}", tags=["Películas"], status_code=200)
def delete_movie(id: int):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(
            status_code=404, content={"Mensaje": "No se encuentra el recurso"}
        )
    db.delete(data)
    db.commit()
    return JSONResponse(
        content={
            "mensaje": "Se ha eliminado la película",
            "data": jsonable_encoder(data),
        }
    )
