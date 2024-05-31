from flask_jwt_extended import create_access_token, JWTManager
from app.Models.User import User

jwt = JWTManager()

@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    # Implementa la carga del usuario desde la base de datos según el 'identity' proporcionado
    user = User.query.get(identity)
    return user

def authenticate_user(email, password):
    # Implementa la autenticación del usuario aquí
    user = User.query.filter_by(email=email, password=password).first()

    if user:
        token = create_access_token(identity=user.id)
        return user, token
    else:
        return None, None
    