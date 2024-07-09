import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(250), nullable=False)
    apellido = Column(String(250), nullable=False)
    correo_electronico = Column(String(250), nullable=False, unique=True)
    fecha_suscripcion = Column(String(250), nullable=False)
    contraseña = Column(String(250), nullable=False)
    
    personajes_favoritos = relationship('PersonajeFavorito', back_populates='usuario')
    planetas_favoritos = relationship('PlanetaFavorito', back_populates='usuario')
    vehiculos_favoritos = relationship('VehiculoFavorito', back_populates='usuario')

class Personaje(Base):
    __tablename__ = 'personaje'
    id = Column(Integer, primary_key=True)
    nombre_personaje = Column(String(250), nullable=False)

    personajes_favoritos = relationship('PersonajeFavorito', back_populates='personaje')

class Planeta(Base):
    __tablename__ = 'planeta'
    id = Column(Integer, primary_key=True)
    nombre_planeta = Column(String(250), nullable=False)

    planetas_favoritos = relationship('PlanetaFavorito', back_populates='planeta')

class Vehiculo(Base):
    __tablename__ = 'vehiculo'
    id = Column(Integer, primary_key=True)
    nombre_vehiculo = Column(String(250), nullable=False)

    vehiculos_favoritos = relationship('VehiculoFavorito', back_populates='vehiculo')

class PersonajeFavorito(Base):
    __tablename__ = 'personaje_favorito'
    id = Column(Integer, primary_key=True)
    personaje_id = Column(Integer, ForeignKey('personaje.id'), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)

    personaje = relationship('Personaje', back_populates='personajes_favoritos')
    usuario = relationship('Usuario', back_populates='personajes_favoritos')

class PlanetaFavorito(Base):
    __tablename__ = 'planeta_favorito'
    id = Column(Integer, primary_key=True)
    planeta_id = Column(Integer, ForeignKey('planeta.id'), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)

    planeta = relationship('Planeta', back_populates='planetas_favoritos')
    usuario = relationship('Usuario', back_populates='planetas_favoritos')

class VehiculoFavorito(Base):
    __tablename__ = 'vehiculo_favorito'
    id = Column(Integer, primary_key=True)
    vehiculo_id = Column(Integer, ForeignKey('vehiculo.id'), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)

    vehiculo = relationship('Vehiculo', back_populates='vehiculos_favoritos')
    usuario = relationship('Usuario', back_populates='vehiculos_favoritos')

    def to_dict(self):
        return {}


engine = create_engine('sqlite:///starwars.db')
Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()


personajes_iniciales = [
    {'nombre_personaje': 'Luke Skywalker'},
    {'nombre_personaje': 'Darth Vader'},
    {'nombre_personaje': 'Leia Organa'},
    {'nombre_personaje': 'Han Solo'},
    
]

planetas_iniciales = [
    {'nombre_planeta': 'Tatooine'},
    {'nombre_planeta': 'Alderaan'},
    {'nombre_planeta': 'Hoth'},
    {'nombre_planeta': 'Dagobah'},
    
]


for personaje_data in personajes_iniciales:
    personaje = Personaje(**personaje_data)
    session.add(personaje)


for planeta_data in planetas_iniciales:
    planeta = Planeta(**planeta_data)
    session.add(planeta)


session.commit()


render_er(Base, 'diagram.png')
