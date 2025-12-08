from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UsuarioModel
from main.auth.decorators import role_required
from flask_jwt_extended import get_jwt_identity, get_jwt

class Usuario(Resource):

# OBTENER USUARIO EN ESPECÍFICO (Sólo admin y el mismo usuario)
    @role_required(roles = ["admin", "cliente"])
    def get(self, id):

        # Filtrando el usuario según el id
        usuario = db.session.query(UsuarioModel).get_or_404(id)

        # AUTENTICACIÓN:
        current_user_id = int(get_jwt_identity())
        claims = get_jwt()
        current_role = claims["role"]

        if usuario.role == "cliente":   # IF: Si el usuario que estamos consultando es un cliente
            
            if current_user_id == usuario.id or current_role == "admin":    # IF: Si quien hace la consulta es el mismo cliente o un admin
                return usuario.to_json(), 201
            else:
                return "Unauthorized", 401
        
        else:
            return "Vacío", 404        
        
        
# ELIMINAR USUARIO EN ESPECÍFICO (Sólo admin)    
    @role_required(roles = ["admin"])
    def delete(self, id):

        # Filtrando usuario según el id
        usuario = db.session.query(UsuarioModel).get_or_404(id)

        # Eliminación del usuario y actualización de la db
        try:
            db.session.delete(usuario)
            db.session.commit()
            return "Usuario eliminado", 201
        
        except:
            return "Vacío", 404
        

# MODIFICAR USUARIO EN ESPECÍFICO (Sólo admin y el mismo usuario)    
    @role_required(roles = ["admin", "cliente"])
    def put(self, id):

        # Filtrando el usuario con cierto id
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        data = request.get_json().items()

        # AUTENTICACIÓN:
        current_user_id = int(get_jwt_identity())
        claims = get_jwt()
        current_role = claims["role"]

        # Error si el usuario actual no es dueño del id o no es admin
        if current_user_id != usuario.id and current_role != "admin":
            return "Vacio", 401
        
        # LÓGICA DE MODIFICACIÓN DE USUARIO:
        campos_permitidos = ["nombre", "apellido", "email", "telefono"]

        # Asignar valores al objeto cliente y evita modificar campos delicados, como role
        for key, value in data:
            if key in campos_permitidos or current_role == "admin":
                setattr(usuario, key, value)

            else:
                return "Unauthorized", 401

        # Actualización de la db
        try:
            db.session.add(usuario)
            db.session.commit()
            return usuario.to_json(), 201
        
        except:
            return "Vacío", 404

class Usuarios(Resource):
    
# OBTENER USUARIOS (Sólo admin)
    @role_required(roles = ["admin"])
    def get(self):
        # PAGINACIÓN: Leer los parámetros dados en la URL (page y per_page)
        page = request.args.get("page", default = 1, type = int)
        per_page = request.args.get("per_page", default = 5, type = int)

        # PAGINACIÓN: Implementar paginación (Flask-SQLAlchemy)
        usuarios = UsuarioModel.query.paginate(
            page = page,
            per_page = per_page,
            error_out = False
        )

        # SALIDA: Retorno del json con los datos de la página solicitada
        return jsonify({
            "Usuarios": [usuario.to_json() for usuario in usuarios.items],
            "Total": usuarios.total,
            "Pages": usuarios.pages,
            "Page": page
        })


# CREAR USUARIO (Sólo admin)
    @role_required(roles = ["admin"])
    def post(self):
        # Lectura de Json y creación del objeto Usuario
        usuario = UsuarioModel.from_json(request.get_json())
        
        # Actualización de la db
        db.session.add(usuario)
        db.session.commit()
        
        return usuario.to_json(), 201