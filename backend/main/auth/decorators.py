from .. import jwt
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from main.models import UsuarioModel

def role_required(roles):
    def decorator(function):
        def wrapper(*args, **kwargs):

            # Verificar que el JWT sea correcto
            verify_jwt_in_request()

            # Obtener los claims que están dentro del JWT
            claims = get_jwt()

            # Verificar que el rol sea el permitido
            if claims['role'] in roles:
                return function(*args, **kwargs)
            
            else:
                return "Rol not allowed", 403
            
        return wrapper
    return decorator


@jwt.additional_claims_loader
def add_claims_to_access_token(user_id):
    usuario = UsuarioModel.query.get(int(user_id))
    return {
        "id": usuario.id,
        "role": usuario.role,
        "email": usuario.email
    }