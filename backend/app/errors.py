from flask import jsonify


def error(message, status=400, details=None):
    payload = {"error": message}

    if details:
        payload["details"] = details

    return jsonify(payload), status


def required(data, fields):
    missing = [
        field
        for field in fields
        if data.get(field) in (None, "")
    ]

    return missing