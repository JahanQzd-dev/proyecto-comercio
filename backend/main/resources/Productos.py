from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import ProductoModel
from main.auth.decorators import role_required
from flask_jwt_extended import get_jwt_identity, get_jwt

class Producto(Resource):
    
# OBTENER PRODUCTO EN ESPECÍFICO (Sin autorización)    
    def get(self, id):
        
        # Filtrando el producto según el id
        producto = db.session.query(ProductoModel).get_or_404(id)
        
        # SALIDA:
        try:
            return producto.to_json()
        except:
            return "Resource not found", 404
        
# MODIFICAR UN PRODUCTO EN ESPECÍFICO (Sólo admin)
    @role_required(roles = ["admin"])
    def put(self, id):

        # Filtrando el producto según el id, y lectura del Json
        producto = db.session.query(ProductoModel).get_or_404(id)
        data = request.get_json().items()
        
        # Asignar valores al objeto Producto
        for key, value in data:
            setattr(producto, key, value)

        # Actualización de la db
        try:
            db.session.add(producto)
            db.session.commit()
            return producto.to_json(), 201
        
        except:
            return "Bad request", 400
        
# ELIMINAR UN PRODUCTO EN ESPECÍFICO (Sólo admin)  
    def delete(self, id):

        # Filtrando el producto según el id
        producto = db.session.query(ProductoModel).get_or_404(id) 

        # Actualización de la db
        try:
            db.session.delete(producto)
            db.session.commit()

        except: "Bad request", 400



class Productos(Resource):

# OBTENER PRODUCTO EN ESPECÍFICO (Sin autorización)
    def get(self):

        # PAGINACIÓN: Leer los parámetros dados en la URL (page y per_page)
        page = request.args.get("page", default = 1, type = int)    
        per_page = request.args.get("per_page", default = 3, type = int) 
        
        # PAGINACIÓN: Implementar paginación (Flask-SQLAlchemy)
        productos = ProductoModel.query.paginate(   
            page = page,
            per_page = per_page,
            error_out = False
        )

        # SALIDA: Retorno del json con los datos de la página solicitada
        return jsonify({
            "Productos": [producto.to_json() for producto in productos.items],
            "Total": productos.total,
            "Pages": productos.pages,
            "Page": page
        })


# CREAR UN PRODUCTO (Sólo admin)
    @role_required(roles = ["admin"])    
    def post(self):
        # Lectura del Json
        producto = ProductoModel.from_json(request.get_json())
        
        # Actualización de la db
        db.session.add(producto)
        db.session.commit()

        return producto.to_json(), 201