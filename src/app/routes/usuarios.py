from flask import request, jsonify

@app.route('/api/usuarios', methods=['GET'])
def get_usuarios():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM RegistroUsuarios')
        data = cursor.fetchall()
        conn.close()

        result = [{'id': row[0], 'nombre': row[1], 'apellido': row[2], 'correo': row[3], 'telefono': row[4], 'fecha_nacimiento': row[5], 'preferencias_alimenticias': row[6]} for row in data]

        return jsonify({'data': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/usuarios/<int:id>', methods=['GET'])
def get_usuario(id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM RegistroUsuarios WHERE id = %s', (id,))
        data = cursor.fetchone()
        conn.close()

        if data:
            result = {'id': data[0], 'nombre': data[1], 'apellido': data[2], 'correo': data[3], 'telefono': data[4], 'fecha_nacimiento': data[5], 'preferencias_alimenticias': data[6]}
            return jsonify({'usuario': result})
        else:
            return jsonify({'mensaje': 'Usuario no encontrado'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/usuarios', methods=['POST'])
def create_usuario():
    try:
        new_usuario = request.json
        nombre = new_usuario.get('nombre')
        apellido = new_usuario.get('apellido')
        correo = new_usuario.get('correo')
        telefono = new_usuario.get('telefono')
        fecha_nacimiento = new_usuario.get('fecha_nacimiento')
        preferencias_alimenticias = new_usuario.get('preferencias_alimenticias')

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute('INSERT INTO RegistroUsuarios (nombre, apellido, correo, telefono, fecha_nacimiento, preferencias_alimenticias) VALUES (%s, %s, %s, %s, %s, %s)', (nombre, apellido, correo, telefono, fecha_nacimiento, preferencias_alimenticias))
        conn.commit()
        conn.close()

        return jsonify({'mensaje': 'Usuario creado correctamente'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/usuarios/<int:id>', methods=['PUT'])
def update_usuario(id):
    try:
        updated_usuario = request.json
        nombre = updated_usuario.get('nombre')
        apellido = updated_usuario.get('apellido')
        correo = updated_usuario.get('correo')
        telefono = updated_usuario.get('telefono')
        fecha_nacimiento = updated_usuario.get('fecha_nacimiento')
        preferencias_alimenticias = updated_usuario.get('preferencias_alimenticias')

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute('UPDATE RegistroUsuarios SET nombre = %s, apellido = %s, correo = %s, telefono = %s, fecha_nacimiento = %s, preferencias_alimenticias = %s WHERE id = %s', (nombre, apellido, correo, telefono, fecha_nacimiento, preferencias_alimenticias, id))
        conn.commit()
        conn.close()

        return jsonify({'mensaje': 'Usuario actualizado correctamente'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/usuarios/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute('DELETE FROM RegistroUsuarios WHERE id = %s', (id,))
        conn.commit()
        conn.close()

        return jsonify({'mensaje': 'Usuario eliminado correctamente'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500



