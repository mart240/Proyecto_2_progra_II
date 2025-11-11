# Definición de modelos clases etc.
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Cliente(Base):
    __tablename__ = 'clientes'
    
    id = Column(Integer, primary_key=True, autoincrement=True )
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    email = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    direccion = Column(String, nullable=False)

class Pedido(Base):
    __tablename__ = 'pedidos'
    
    id = Column(Integer, primary_key=True, autoincrement=True )
    descripcion = Column(String, nullable=False)
    cliente_email = Column(String, ForeignKey('clientes.email', onupdate="CASCADE"), nullable=False)
    cliente = relationship("Cliente", back_populates="pedidos")

class Ingrediente(Base):
    __tablename__ = 'ingredientes'
    
    id = Column(Integer, primary_key=True, autoincrement=True )
    nombre = Column(String, nullable=False)
    cantidad = Column(Integer, nullable=False)

class Menu(Base):
    __tablename__ = 'menus'
    
    id = Column(Integer, primary_key=True, autoincrement=True )
    nombre = Column(String, nullable=False)
    precio = Column(Integer, nullable=False)
    icono_path = Column(String, nullable=True)
    ingredientes = relationship("ingrediente", secondary="ingrediente_menu", back_populates="menus")

