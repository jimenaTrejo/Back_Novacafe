# modelo.py
from sqlalchemy import Column, Integer, String, Text, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class CatalogoProductos(Base):
    __tablename__ = 'catalogo_productos'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(Text)
    detalles_nutricionales = Column(Text)
    precio = Column(DECIMAL(10, 2), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'detalles_nutricionales': self.detalles_nutricionales,
            'precio': float(self.precio)
        }
