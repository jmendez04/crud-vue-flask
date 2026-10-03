from decimal import Decimal, InvalidOperation

from flask import jsonify, request

from ..errors import error, required
from ..extensions import db
from ..models import Producto
from . import api_bp


def producto_data(data):
    missing = required(data, ["nombre", "precio", "stock"])

    if missing:
        return None, error(
            "Faltan campos obligatorios",
            details=missing
        )

    try:
        precio = Decimal(str(data["precio"]))
        stock = int(data["stock"])

    except (InvalidOperation, TypeError, ValueError):
        return None, error(
            "Precio o stock no válidos"
        )

    if precio < 0 or stock < 0:
        return None, error(
            "Precio y stock deben ser mayores o iguales a cero"
        )

    return {
        "nombre": str(data["nombre"]).strip(),
        "descripcion": str(
            data.get("descripcion", "")
        ).strip(),
        "precio": precio,
        "stock": stock,
        "activo": bool(data.get("activo", True)),
    }, None


@api_bp.get("/productos")
def listar_productos():
    productos = Producto.query.order_by(
        Producto.id.desc()
    ).all()

    return jsonify([
        producto.to_dict()
        for producto in productos
    ])


@api_bp.get("/productos/<int:producto_id>")
def obtener_producto(producto_id):
    producto = db.get_or_404(
        Producto,
        producto_id
    )

    return jsonify(producto.to_dict())


@api_bp.post("/productos")
def crear_producto():
    data, response = producto_data(
        request.get_json(silent=True) or {}
    )

    if response:
        return response

    producto = Producto(**data)

    db.session.add(producto)
    db.session.commit()

    return jsonify(producto.to_dict()), 201


@api_bp.put("/productos/<int:producto_id>")
def actualizar_producto(producto_id):
    producto = db.get_or_404(
        Producto,
        producto_id
    )

    data, response = producto_data(
        request.get_json(silent=True) or {}
    )

    if response:
        return response

    for key, value in data.items():
        setattr(producto, key, value)

    db.session.commit()

    return jsonify(producto.to_dict())


@api_bp.delete("/productos/<int:producto_id>")
def eliminar_producto(producto_id):
    producto = db.get_or_404(
        Producto,
        producto_id
    )

    if producto.pedidos:
        return error(
            "No se puede eliminar un producto con pedidos",
            409
        )

    db.session.delete(producto)
    db.session.commit()

    return "", 204