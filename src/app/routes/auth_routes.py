# rutas.py
from flask import Blueprint, jsonify, request
from app.services.Product_service import get_all_products, add_product

catalogo_routes = Blueprint("catalogo_routes", __name__)

@catalogo_routes.route("/catalogo_alimentos", methods=["GET"])
def get_products():
    productos = get_all_products()
    return jsonify(productos)

@catalogo_routes.route("/catalogo_alimentos", methods=["POST"])
def create_product():
    data = request.json
    nuevo_producto = add_product(data)
    return jsonify(nuevo_producto), 201

# Agrega otras rutas aquí, como la actualización y eliminación de productos
