from flask import Blueprint, jsonify
from ..services.Product_service import get_all_products
from app.services.Product_service import get_all_products  # Importación absoluta

# from app.Services.Product_service import get_product_by_id, get_all_products

product_routes = Blueprint("product_routes", __name__)
@product_routes.route("/products", methods=["GET"])
def get_products():
    products = get_all_products()
    return jsonify(products)



@product_routes.route('/products')
def products():
    return 'Lista de productos'
