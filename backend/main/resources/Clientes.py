from flask_restful import Resource
from flask import jsonify, request
from .. import db
from main.models import UsuarioModel
from main.auth.decorators import role_required
from flask_jwt_extended import get_jwt_identity, get_jwt


class Clientes(Resource):

# OBTENER CLIENTES (Sólo admin)
    @role_required(roles = ["admin"])  
    def get(self):

        # PAGINACIÓN: Leer los parámetros dados en la URL (page y per_page)
        page = request.args.get("page", default = 1, type = int)
        per_page = request.args.get("per_page", default = 5, type = int)

        # Filtrado de clientes
        query = UsuarioModel.query.filter(UsuarioModel.role == "cliente")

        # PAGINACIÓN: Implementar paginación (Flask-SQLAlchemy)
        clientes = query.paginate(
            page = page,
            per_page = per_page,
            error_out = False
        )

        # SALIDA: Retorno del json con los datos de la página solicitada
        return jsonify({
            "Clientes": [cliente.to_json() for cliente in clientes.items],
            "Total": clientes.total,
            "Pages": clientes.pages,
            "Page": page
        })


# CREAR CLIENTE (Cualquier persona)
    def post(self):
        # Lectura de Json y creación del objeto Cliente
        cliente = UsuarioModel.from_json(request.get_json())
        cliente.role = "cliente"    # Valor por default
        
        # Actualización de la db
        db.session.add(cliente)
        db.session.commit()
        return cliente.to_json(), 201



class Cliente(Resource):
    
# OBTENER CLIENTE ESPECÍFICO (Sólo admin y el mismo cliente)
    @role_required(roles = ["admin", "cliente"])
    def get(self, id):

        # Filtrado del Usuario con cierto id
        cliente = db.session.query(UsuarioModel).get_or_404(id) 

        # AUTENTICACIÓN: 
        current_user_id = int(get_jwt_identity())   # Obtener el id del cliente a través del JWT
        claims = get_jwt()     # Diccionario con atributos del cliente 
        current_role = claims["role"]   # Obtener el rol del cliente

        if cliente.role == "cliente":   # IF: Si el usuario que estamos consultando es un cliente
            
            if current_user_id == cliente.id or current_role == "admin":    # IF: Si quien hace la consulta es el mismo cliente o un admin
                return cliente.to_json(), 201
            else:
                return "Unauthorized", 401
        
        else:
            return "Vacío", 404
       
        
# MODIFICAR CLIENTE ESPECÍFICO (Sólo admin y el mismo usuario)
    @role_required(roles = ["admin", "cliente"])    
    def put(self, id):

        # Filtrado del usuario con cierto id
        cliente = db.session.query(UsuarioModel).get_or_404(id) 
        data = request.get_json().items()

        # AUTENTICACIÓN:
        current_user_id = int(get_jwt_identity())   # Obtener el id del cliente a través del JWT
        claims = get_jwt()   # Diccionario con atributos del cliente 
        current_role = claims["role"]

        # Error si el usuaro solicitado NO es cliente
        if cliente.role != "cliente":
            return "Vacio", 404
        
        # Error si el usuario actual no es dueño del id o no es admin
        if current_user_id != cliente.id and current_role != "admin":
            return "Vacio", 401

        # LÓGICA DE MODIFICACIÓN DE CLIENTE:  
        campos_permitidos = ["nombre", "apellido", "email", "telefono"]
                        
        # Asignar valores al objeto cliente y evita modificar campos delicados, como role
        for key, value in data:
            if key in campos_permitidos or current_role == "admin":
                setattr(cliente, key, value)
                    
            else:
                return "Unauthorized", 401

        # Actualización de la db
        try:
            db.session.add(cliente)
            db.session.commit()
            return cliente.to_json(), 201
                
        except:
            return "Vacío", 404
                
            
# ELIMINAR CLIENTE EN ESPECÍFICO (Sólo el admin)
    @role_required(roles = ["admin"])
    def delete(self, id):

        # Filtrando el usuario con cierto id
        cliente = db.session.query(UsuarioModel).get_or_404(id)

        #Actualización de la db
        try:
            db.session.delete(cliente)
            db.session.commit()
            return "Cliente eliminado", 201
        
        except:
            return "Vacío", 404