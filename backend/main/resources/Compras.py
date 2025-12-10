from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import CompraModel, UsuarioModel
from main.auth.decorators import role_required
from flask_jwt_extended import get_jwt_identity, get_jwt

class Compra(Resource):
    
# OBTENER COMPRA EN ESPECÍFICO (Sólo admin y el cliente dueño de la compra)
    @role_required(roles = ["admin", "cliente"])
    def get(self, id):

        # Filtrando la compra según el id
        compra = db.session.query(CompraModel).get_or_404(id)

        # AUTENTICACIÓN:
        current_user_id = int(get_jwt_identity())   # Obtener el id del cliente a través del JWT
        claims = get_jwt()     # Diccionario con atributos del cliente 
        current_role = claims["role"]   # Obtener el rol del cliente

        if current_user_id == compra.usuario_id or current_role == "admin": # IF: Si quien hace la consulta es el mismo cliente o un admin
            return compra.to_json(), 201
        
        else:
            return "Unauthorized", 401
        

# MODIFICAR COMPRA EN ESPECÍFICO (Sólo admin)    
    @role_required(roles = ["admin"])
    def put(self, id):
        
        # Filtrando compra según el id
        compra = db.session.query(CompraModel).get_or_404(id)
        data = request.get_json().items()

        # LÓGICA DE MODIFICACIÓN DE COMPRA
        # Asignar valores al objeto compra
        for key, value in data:
            setattr(compra, key, value)
        
        # Actualización de la db
        try:
            db.session.add(compra)
            db.session.commit()
            return compra.to_json(), 201
        
        except:
            return "Bad request", 400
        

# ELIMINAR COMPRA EN ESPECÍFICO (Sólo admin)
    @role_required(roles = ["admin"])    
    def delete(self, id):

        # Filtrando la compra según el id
        compra = db.session.query(CompraModel).get_or_404(id)

        # Actualización de la db
        try:
            db.session.delete(compra)
            db.session.commit()
            return "Compra eliminada", 204
        
        except:
            return "Bad request", 400


class Compras(Resource):
    
# CREAR UNA COMPRA (Sólo admin)
    @role_required(roles = ["admin"])
    def post(self):
        # Lectura del Json y asignación del id del usuario
        data = request.get_json()
        usuario = UsuarioModel.query.get(data.get("usuario_id"))

        # IF: Error si el usuario no existe
        if not usuario:
            return "User not found", 404
        
        # Creación del objeto Compra y actualización de la db
        try:
            compra = CompraModel.from_json(data)
            db.session.add(compra)
            db.session.commit()
            return compra.to_json(), 201
        
        except:
            db.session.rollback()
            return "error", 500


# OBTENER COMPRAS (Sólo admin) 
    @role_required(roles = ["admin"])
    def get(self):
        
        #PAGINACIÓN: Leer los parámetros dados en la URL (page y per_page)
        page = request.args.get("page", default = 1, type = int)
        per_page = request.args.get("per_page", default = 2, type = 1)

        # PAGINACIÓN: Implementar paginación (Flask-SQLAlchemy)
        compras = CompraModel.query.paginate(
            page = page,
            per_page = per_page,
            error_out = False
        )

        # SALIDA: Retorno del json con los datos de la página solicitada
        return jsonify({
            "Compras": [compra.to_json() for compra in compras.items],
            "Total": compras.total,
            "Pages": compras.pages,
            "Page": page
        })