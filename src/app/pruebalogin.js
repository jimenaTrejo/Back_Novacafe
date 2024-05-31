// Datos del usuario para iniciar sesión
const datosUsuario = {
    correo: 'correo@institucional.com',
    contrasena: 'contraseña'
};

// Opciones para la solicitud POST
const opciones = {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(datosUsuario)
};

// Realizar la solicitud POST al punto final de inicio de sesión
fetch('/api/login', opciones)
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la solicitud');
        }
        return response.json();
    })
    .then(data => {
        console.log('Respuesta del servidor:', data);
        // Aquí puedes manejar la respuesta del servidor, como redirigir a otra página o mostrar un mensaje de éxito
    })
    .catch(error => {
        console.error('Error:', error);
        // Aquí puedes manejar errores, como mostrar un mensaje de error al usuario
    });
