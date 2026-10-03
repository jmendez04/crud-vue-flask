from flask import Blueprint

api_bp = Blueprint("api", __name__)

from . import clientes, productos  # noqa: E402, F401