from bd.database import Base
from sqlalchemy import Column, Integer, String, Float

class Movie(Base):
    __tablename__= 'movies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String)
    resumen = Column(String)
    anio = Column(Integer)
    rating = Column(Float)
    categoria = Column(String)
    