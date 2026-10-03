from flask import jsonify, request

from ..errors import error, required
from ..extensions import db
from ..models import Cliente, Pedido, Producto
from . import api_bp


@api_bp.get("/pedidos")
def listar_pedidos():
    pedidos = Pedido.query.order_by(Pedido.id.desc()).all()

    return jsonify([
        pedido.to_dict()
        for pedido in pedidos
    ])


@api_bp.get("/pedidos/<int:pedido_id>")
def obtener_pedido(pedido_id):
    pedido = db.get_or_404(Pedido, pedido_id)

    return jsonify(pedido.to_dict())


def pedido_data(data):
    missing = required(
        data,
        ["cliente_id", "producto_id", "cantidad"]
    )

    if missing:
        return None, error(
            "Faltan campos obligatorios",
            details=missing
        )

    try:
        cliente_id = int(data["cliente_id"])
        producto_id = int(data["producto_id"])
        cantidad = int(data["cantidad"])

    except (TypeError, ValueError):
        return None, error(
            "Los identificadores y la cantidad deben ser enteros"
        )

    if cantidad <= 0:
        return None, error(
            "La cantidad debe ser mayor que cero"
        )

    cliente = db.session.get(
        Cliente,
        cliente_id
    )

    producto = db.session.get(
        Producto,
        producto_id
    )

    if not cliente or not producto:
        return None, error(
            "Cliente o producto no encontrado",
            404
        )

    if producto.stock < cantidad:
        return None, error(
            "Stock insuficiente",
            409
        )

    return {
        "cliente": cliente,
        "producto": producto,
        "cantidad": cantidad,
    }, None


@api_bp.post("/pedidos")
def crear_pedido():
    data, response = pedido_data(
        request.get_json(silent=True) or {}
    )

    if response:
        return response

    data["producto"].stock -= data["cantidad"]

    pedido = Pedido(
        cliente=data["cliente"],
        producto=data["producto"],
        cantidad=data["cantidad"],
        estado="pendiente",
    )

    db.session.add(pedido)
    db.session.commit()

    return jsonify(pedido.to_dict()), 201


@api_bp.put("/pedidos/<int:pedido_id>")
def actualizar_pedido(pedido_id):
    pedido = db.get_or_404(
        Pedido,
        pedido_id
    )

    data = request.get_json(silent=True) or {}
    estado = data.get("estado")

    estados = {
        "pendiente",
        "pagado",
        "enviado",
        "cancelado",
    }

    if estado not in estados:
        return error(
            "Estado no válido",
            details=sorted(estados)
        )

    pedido.estado = estado
    db.session.commit()

    return jsonify(pedido.to_dict())


@api_bp.delete("/pedidos/<int:pedido_id>")
def eliminar_pedido(pedido_id):
    pedido = db.get_or_404(
        Pedido,
        pedido_id
    )

    if pedido.estado != "cancelado":
        return error(
            "Solo se pueden eliminar pedidos cancelados",
            409
        )

    db.session.delete(pedido)
    db.session.commit()

    return "", 204