from flask import Flask, request,jsonify    
from flask_cors import CORS
# from models.products import CatalogoProductos
# from flaskext.mysql import MySQL
import mysql.connector
# from config import config
from flask_sqlalchemy import SQLAlchemy
import json



app = Flask(__name__)

CORS(app)  # Habilita CORS para toda la aplicación
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'cafenova',
}
# Conecta con MySQL
# conn = mysql.connector.connect(**db_config)
# cursor = conn.cursor()

# conn.commit()
# conn.close()

conexion = mysql.connector.connect(**db_config)


@app.route('/api/productos', methods=['GET'])
def get_data():
    try:
        # Conecta con MySQL
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        # Obtiene todos los datos de la tabla
        cursor.execute('SELECT alimento_id, nombre, descripcion, detalles_nutricionales, precio, imagenes FROM CatalogoAlimentos')
        data = cursor.fetchall()
        conn.close()
        # Convierte los resultados a un formato JSON
        result = [{'alimento_id': row[0], 'nombre': row[1], 'descripcion': row[2], 'detalles_nutricionales': row[3], 'precio':row[4],'imagenes': row[5],} for row in data]
        return jsonify({'data': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/verCarrito', methods=['GET'])
def ver_carrito():
    try:
        # Conectar con MySQL
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        # Obtener usuario_id del cuerpo de la solicitud
        usuario_id = request.args.get('usuario_id')
        # Modificar la consulta para obtener solo las columnas requeridas
        cursor.execute('SELECT  alimento_id, nombre_alimento, precio_alimento, imagen_alimento, cantidad FROM carritodecompras WHERE usuario_id = %s', (usuario_id,))
        carrito = cursor.fetchall()
        conn.close()
        # Modificar los datos de la consulta para agregar los campos adicionales
        result = [{'alimento_id': row['alimento_id'], 'nombre_alimento': row['nombre_alimento'], 'precio_alimento': row['precio_alimento'], 'imagen_alimento': row['imagen_alimento'], 'cantidad': row['cantidad']} for row in carrito]
        return jsonify({'carrito': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/agregarCarrito', methods=['POST'])
def agregar_al_carrito():
    try:
        # Conectar con MySQL
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        # Obtener datos del cuerpo de la solicitud
        data = request.json
        usuario_id = data.get('usuario_id')
        alimento_id = data.get('alimento_id')
        cantidad = data.get('cantidad')
        # Insertar el producto en el carrito de compras
        # cursor.execute('INSERT INTO AgregarProductoAlCarrito (usuario_id, alimento_id, cantidad) VALUES (%s, %s, %s)', (usuario_id, alimento_id, cantidad))
        cursor.callproc('AgregarProductoAlCarritot', (usuario_id, alimento_id, cantidad))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Producto agregado al carrito de compras correctamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/eliminarProductoCarrito', methods=['DELETE'])
def eliminar_del_carrito():
    try:
        # Conectar con MySQL
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Obtener datos del cuerpo de la solicitud
        data = request.json
        alimento_id = data.get('alimento_id')
        
        # Verificar si alimento_id está presente en la solicitud
        if alimento_id is None:
            return jsonify({'error': 'No se proporcionó alimento_id'}), 400
        
        # Llamar al procedimiento almacenado para eliminar el producto del carrito
        cursor.callproc('EliminarProductoDelCarrito', (alimento_id,))
        
        # Verificar si se eliminó correctamente el producto del carrito
        cursor.execute("SELECT ROW_COUNT();")
        rows_affected = cursor.fetchone()[0]
        
        if rows_affected == 0:
            return jsonify({'error': 'El producto no existe en el carrito'}), 404
        
        # Confirmar la transacción y cerrar la conexión
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Producto eliminado del carrito de compras correctamente'}), 200
    except mysql.connector.Error as e:
        return jsonify({'error': str(e)}), 500

    
    

@app.route('/api/ordenCompra', methods=['POST'])
def generar_orden_compra():
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.json
        usuario_id = data.get('usuario_id')
        
        # Conectar con MySQL
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Llamar al procedimiento almacenado para generar la orden de compra
        cursor.callproc('GenerarOrdenDeCompra', (usuario_id,))

        # Obtener el resultado del procedimiento almacenado
        result = next(cursor.stored_results())
        orden_info = result.fetchone()

        conn.commit()
        conn.close()

        # Devolver una respuesta con la información de la orden generada
        return jsonify({
            'codigo_orden': orden_info[0],
            'total': float(orden_info[1]) if orden_info[1] is not None else None,
            'message': 'Orden de compra generada correctamente'
        }), 200

    except Exception as e:
        # Devolver una respuesta de error si ocurre alguna excepción
        return jsonify({'error': str(e)}), 500
    
    

@app.route('/api/pedidos', methods=['GET'])
def get_pedidos():
    try:
        # Conectar con MySQL
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        # Obtener usuario_id del cuerpo de la solicitud
        usuario_id = request.args.get('usuario_id')
        # Consulta SQL para obtener los datos de la tabla Pedidos
        cursor.execute("SELECT precio_alimento, cantidad, fecha_pedido, nombre_alimento, imagen_alimento, codigo_orden FROM Pedidos WHERE usuario_id = %s", (usuario_id,))
        pedidos = cursor.fetchall()
        conn.close()
        # Obtener los datos de los pedidos
        result = [{'precio_alimento': row['precio_alimento'], 'cantidad': row['cantidad'], 'fecha_pedido': row['fecha_pedido'], 'nombre_alimento': row['nombre_alimento'], 'imagen_alimento': row['imagen_alimento'], 'codigo_orden': row['codigo_orden']} for row in pedidos]
        return jsonify({'pedidos': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/obtenerPedidos', methods=['GET'])
def get_ordenesPedidos():
    try:
        # Conectar con MySQL
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        # Obtener usuario_id del cuerpo de la solicitud
        # Consulta SQL para obtener los datos de la tabla Pedidos
        cursor.execute("SELECT precio_alimento, cantidad, fecha_pedido, nombre_alimento, imagen_alimento, codigo_orden FROM Pedidos")
        Ordenpedidos = cursor.fetchall()
        conn.close()
        # Obtener los datos de los pedidos
        result = [{'precio_alimento': row['precio_alimento'], 'cantidad': row['cantidad'], 'fecha_pedido': row['fecha_pedido'], 'nombre_alimento': row['nombre_alimento'], 'imagen_alimento': row['imagen_alimento'], 'codigo_orden': row['codigo_orden']} for row in Ordenpedidos]
        return jsonify({'pedidos': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
@app.route('/api/eliminarOrdenPedido/<string:codigo_orden>', methods=['DELETE'])
def eliminar_orden_pedido(codigo_orden):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM Pedidos WHERE codigo_orden = %s", (codigo_orden,))
        conn.commit()
        conn.close()

        return jsonify({'mensaje': 'Orden de pedido eliminada correctamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500




    
@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json
        correo = data.get('correo')
        contrasena = data.get('contrasena')
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        # Busca al usuario por correo y contraseña
        cursor.execute('SELECT * FROM Usuarios WHERE correo = %s AND Contrasena = %s', (correo, contrasena))
        usuario = cursor.fetchone()
        if usuario:
            usuario_info = {
                'id': usuario[0],
                'nombre': usuario[1],
                'apellido': usuario[2],
                'correo': usuario[3],
                'telefono': usuario[4], 
                'fecha_nacimiento': usuario[5],
                'preferencias_alimenticias': usuario[6],
                'tipo_usuario_id': usuario[7],
                'contrasena': usuario[8]
            }
            # Determina el tipo de usuario y devuelve información adicional si es necesario
            if usuario_info['tipo_usuario_id'] == '1':
                usuario_info['tipo_usuario'] = 'administrador'
                # Puedes agregar más información específica para administradores si es necesario
            elif usuario_info['tipo_usuario_id'] == '2':
                usuario_info['tipo_usuario'] = 'cliente'
                # Puedes agregar más información específica para clientes si es necesario
            return jsonify({'usuario': usuario_info})
        else:
            return jsonify({'mensaje': 'Correo o contraseña incorrectos'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/api/crearUsuario', methods=['POST'])
def crear_usuario():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        datos_usuario = request.json
        nombre = datos_usuario.get('nombre')
        apellido = datos_usuario.get('apellido')
        contrasena = datos_usuario.get('contrasena')
        correo = datos_usuario.get('correo')
        telefono = datos_usuario.get('telefono')
        tipo_usuario_id = datos_usuario.get('tipo_usuario_id')
        fecha_nacimiento = datos_usuario.get('fecha_nacimiento')
        preferencias_alimenticias = datos_usuario.get('preferencias_alimenticias')     
        
        cursor.callproc("CrearUsuario", (nombre, apellido, contrasena, correo, telefono, tipo_usuario_id, fecha_nacimiento, preferencias_alimenticias))

        conexion.commit()
        cursor.close()
        return jsonify({'mensaje': 'Usuario creado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/api/actualizarUsuario', methods=['POST'])
def actualizar_usuario():
    datos_usuario = request.json
    cursor = conexion.cursor()
    cursor.callproc("ActualizarUsuario", (
        datos_usuario['usuario_id'],
        datos_usuario['nombre'],
        datos_usuario['apellido'],
        datos_usuario['contrasena'],
        datos_usuario['correo'],
        datos_usuario['telefono'],
        datos_usuario['tipo_usuario_id'],
        datos_usuario['fecha_nacimiento'],
        datos_usuario['preferencias_alimenticias']
    ))
    conexion.commit()
    cursor.close()
    return jsonify({'mensaje': 'Información de usuario actualizada exitosamente'})


@app.route('/api/eliminarUsuario', methods=['POST'])
def eliminar_usuario():
    usuario_id = request.json['usuario_id']
    cursor = conexion.cursor()
    cursor.callproc("EliminarUsuario", (usuario_id,))
    conexion.commit()
    cursor.close()
    return jsonify({'mensaje': 'Usuario eliminado exitosamente'})


# @app.route('/api/obtenerUsuario/<int:usuario_id>', methods=['GET'])
# def obtener_usuario():
#     conn = mysql.connector.connect(**db_config)
#     cursor = conn.cursor()
#     datos_usuario = request.json
#     usuario_id = datos_usuario.get('usuario_id')
#     cursor.callproc("ObtenerUsuario", (usuario_id,))
#     usuario = cursor.fetchone()
#     cursor.close()
#     if usuario:
#         return jsonify(usuario)
#     else:
#         return jsonify({'mensaje': 'Usuario no encontrado'}), 404

@app.route('/api/obtenerTodosUsuario', methods=['GET'])
def obtener_Todosusuario():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        
        cursor.execute('SELECT usuario_id, nombre, apellido, correo, telefono, fecha_nacimiento, preferencias_alimenticias FROM usuarios')
        usuario = cursor.fetchall()
        conn.close()
        
        result = [{'usuario_id': row['usuario_id'],'nombre': row['nombre'], 'apellido': row['apellido'], 'correo': row['correo'], 'telefono': row['telefono'], 'fecha_nacimiento': row['fecha_nacimiento'], 'preferencias_alimenticias': row['preferencias_alimenticias']} for row in usuario]

        return jsonify({'mensaje': result}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/api/obtenerUsuario', methods=['GET'])
def obtener_usuario():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        usuario_id = request.args.get('usuario_id')
        
        if usuario_id is None:
            return jsonify({'error': 'El parámetro usuario_id es requerido'}), 400
        
        cursor.execute('SELECT nombre, apellido, correo, telefono, fecha_nacimiento, preferencias_alimenticias, tipo_usuario_id, contrasena FROM usuarios WHERE usuario_id = %s', (usuario_id,))
        usuario = cursor.fetchall()
        conn.close()
        
        result = [{'precio_alimento': row['precio_alimento'], 'cantidad': row['cantidad'], 'fecha_pedido': row['fecha_pedido'], 'nombre_alimento': row['nombre_alimento'], 'imagen_alimento': row['imagen_alimento'], 'codigo_orden': row['codigo_orden']} for row in Ordenpedidos]

        if usuario:
            return jsonify({'usuario': usuario})
        else:
            return jsonify({'mensaje': 'Usuario no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500



# Servicio para insertar un alimento
@app.route('/api/insertarAlimento', methods=['POST'])
def insertar_alimento():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Obtener datos del cuerpo de la solicitud
        data = request.json
        nombre = data.get('nombre')
        descripcion = data.get('descripcion')
        detalles_nutricionales = data.get('detalles_nutricionales')
        precio = data.get('precio')
        imagenes = data.get('imagenes')

        # Llamar al procedimiento almacenado para insertar un alimento
        cursor.callproc("InsertarAlimento", (nombre, descripcion, detalles_nutricionales, precio, imagenes))
        conn.commit()
        conn.close()

        return jsonify({'mensaje': 'Alimento insertado correctamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Servicio para actualizar un alimento
@app.route('/api/actualizarAlimento/<int:alimento_id>', methods=['PUT'])
def actualizar_alimento(alimento_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Obtener datos del cuerpo de la solicitud
        data = request.json
        nombre = data.get('nombre')
        descripcion = data.get('descripcion')
        detalles_nutricionales = data.get('detalles_nutricionales')
        precio = data.get('precio')
        imagenes = data.get('imagenes')

        # Llamar al procedimiento almacenado para actualizar un alimento
        cursor.callproc("ActualizarAlimento", (alimento_id, nombre, descripcion, detalles_nutricionales, precio, imagenes))
        conn.commit()
        conn.close()

        return jsonify({'mensaje': 'Alimento actualizado correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Servicio para eliminar un alimento
@app.route('/api/eliminarAlimento/<int:alimento_id>', methods=['DELETE'])
def eliminar_alimento(alimento_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Llamar al procedimiento almacenado para eliminar un alimento
        cursor.callproc("EliminarAlimento", (alimento_id,))
        conn.commit()
        conn.close()

        return jsonify({'mensaje': 'Alimento eliminado correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500



# Servicio para obtener un alimento por su ID
# @app.route('/api/obtenerAlimento/<int:alimento_id>', methods=['GET'])
# def obtener_alimento_por_id(alimento_id):
#     try:
#         conn = mysql.connector.connect(**db_config)
#         cursor = conn.cursor(dictionary=True)
#         print(alimento_id)
#         # Llamar al procedimiento almacenado para obtener un alimento por su ID
#         cursor.callproc("ObtenerAlimento", (alimento_id,))
#         alimento = cursor.fetchall()
#         print(alimento)
#         conn.close()

#         if alimento:
#             return jsonify({'alimento': alimento})
#         else:
#             return jsonify({'mensaje': 'Alimento no encontrado'}), 404
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

@app.route('/api/obtenerAlimento', methods=['GET'])
def obtener_alimento_por_id():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        alimento_id = request.args.get('alimento_id')
        print(alimento_id)
        if alimento_id is None:
            return jsonify({'error': 'El parámetro alimento_id es requerido'}), 400
        
        cursor.execute('SELECT nombre, descripcion, detalles_nutricionales, precio, imagenes FROM catalogoAlimentos WHERE alimento_id = %s', (alimento_id,))
        alimento = cursor.fetchall()
        conn.close()
        
        if alimento:
            return jsonify({'usuario': alimento})
        else:
            return jsonify({'mensaje': 'Usuario no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500





if __name__ == '__main__':
    app.run(debug=True)

# conexion = MySQL(app)
# print("Conexión a la base de datos establecida con éxito")

# # Configura CORS solo para la ruta /productos
# @app.route("/")
# def hello():
#     return "Hello, Todo List!"

# def get_all_products():
#     productos = CatalogoProductos.query.all()
#     return [producto.serialize() for producto in productos]

# @app.route('/productos', methods=["GET"])
# def get_products():
#     products = get_all_products()
#     return jsonify(products)
    

# # @app.route('/productos/<int:id>', methods=['GET'])
# # def leer_producto(id):
# #     try:
# #         cursor = conexion.connection.cursor()
# #         sql = "SELECT id,title, description, price, stock, category, image FROM producto WHERE id = %s"
# #         cursor.execute(sql, (id,))
# #         datos = cursor.fetchone()

# #         if datos is not None:
# #             producto = {
# #                 'id': datos[0],
# #                 'title': datos[1],
# #                 'description': datos[2],
# #                 'price': datos[3],
# #                 'stock': datos[4],
# #                 'category': datos[5],
# #                 'image': datos[6]
# #             }
# #             return jsonify({'producto': producto, 'mensaje': 'producto leído'})
# #         else:
# #             return jsonify({'mensaje': 'Producto no encontrado'})
# #     except Exception as ex:
# #         return jsonify({'mensaje': 'Error de servidor'})

# if __name__ == '__main__':
#     app.config.from_object(config['development'])
#     app.run()
