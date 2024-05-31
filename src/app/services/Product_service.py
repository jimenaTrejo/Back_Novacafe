# servicio.py
from models.products import CatalogoProductos
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///localhost/a/tu/base/de/datos.db'  # Cambia esto según tu configuración
db = SQLAlchemy(app)

# Importa el modelo después de inicializar db para evitar ciclos de importación
from models.products import CatalogoProductos

def get_all_products():
    productos = CatalogoProductos.query.all()
    return [producto.serialize() for producto in productos]

def add_product(data):
    nuevo_producto = CatalogoProductos(
        nombre=data['nombre'],
        descripcion=data['descripcion'],
        detalles_nutricionales=data['detalles_nutricionales'],
        precio=data['precio']
    )
    #Agrega la libreria que inicializa a db en este archivo
    db.session.add(nuevo_producto)
    db.session.commit()
    return nuevo_producto.serialize()


# Agrega otras funciones de servicio aquí, como actualización y eliminación de productos
