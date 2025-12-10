from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import ProductoCompraModel, ProductoModel, CompraModel
from main.auth.decorators import role_required
from flask_jwt_extended import get_jwt_identity, get_jwt

class ProductoCompra(Resource):

# OBTENER PRODUCTO-COMPRA EN ESPECÍFICO (Sólo admin y cliente dueño de la compra)
    @role_required(roles = ["admin", "cliente"])
    def get(self, id):

        # Filtrando el producto-compra según el id
        producto_compra = db.session.query(ProductoCompraModel).get_or_404(id)

        # AUTENTICACIÓN:
        current_user_id = int(get_jwt_identity())   # Obtener el id del cliente a través del JWT
        claims = get_jwt()  # Diccionario con atributos del cliente 
        current_role = claims["role"]

        # IF: Si el role es cliente, debe ser el dueño de la compra
        if current_role == "cliente":    
            if producto_compra.compra.usuario_id != current_user_id:
                return "Unauthorized", 401
            
        return producto_compra.to_json(), 201
        
# ELIMINAR PRODUCTO-COMPRA EN ESPECÍFICO (Sólo admin)
    @role_required(roles = ["admin"])
    def delete(self, id):
        
        # Filtrando producto-compra según el id
        producto_compra = db.session.query(ProductoCompraModel).get_or_404(id)

        # Actualización de la base de datos
        try:
            db.session.delete(producto_compra)
            db.session.commit()
            return "Eliminado", 201
        
        except:
            return "Bad request", 400
        


class ProductosCompras(Resource):
    
# CREAR PRODUCTO-COMPRA (Sólo admin)   
    @role_required(roles = ["admin"])
    def post(self):

        # Lectura del Json
        data = request.get_json()

        # Asignación del id del producto (error si el producto no existe)
        producto = ProductoModel.query.get(data.get("producto_id"))
        if not producto:
            return "Product not found", 404
        
        # Asignación del id de la compra (error si la compra no existe)
        compra = CompraModel.query.get(data.get("compra_id"))
        if not compra:
            return "Compra not found", 404
        
        # Creación del objeto Producto-Compra y actualización de la db
        try:
            producto_compra = ProductoCompraModel.from_json(request.get_json())
            db.session.add(producto_compra)
            db.session.commit()
            return producto_compra.to_json(), 201
        
        except:
            return "Bad request", 400
    

# OBTENER PRODUCTOS-COMPRAS (Sólo admin y cliente dueño de las compras)
    @role_required(roles = ["admin", "cliente"])
    def get(self):

        # AUTENTICACIÓN:
        current_user_id = int(get_jwt_identity())   # Obtener el id del cliente a través del JWT
        claims = get_jwt()  # Diccionario con atributos del cliente 
        current_role = claims["role"]   # Obtener el rol del cliente

        # ACCESO TOTAL PARA ADMIN:
        if current_role == "admin":
            query = ProductoCompraModel.query

        # ACCESO LIMITADO PARA CLIENTE:
        else:
            query = (
                ProductoCompraModel.query
                .join(CompraModel)  # Unir con la tabla compras
                .filter(CompraModel.usuario_id == current_user_id)  # Filtrando las compras de las que es dueño
            )
        
        # PAGINACIÓN: Leer los parámetros dados en la URL (page y per_page)
        page = request.args.get("page", default = 1, type = int)
        per_page = request.args.get("per_page", default = 3, type = 1)

        # PAGINACIÓN: Implementar paginación (Flask-SQLAlchemy)
        productoscompras = query.paginate(
            page = page,
            per_page = per_page,
            error_out = False
        )

        # SALIDA: Retorno del json con los datos de la página solicitada
        return jsonify({
            "Productos-compras": [productocompra.to_json() for productocompra in productoscompras.items],
            "Total": productoscompras.total,
            "Pages": productoscompras.pages,
            "Page": page
        })