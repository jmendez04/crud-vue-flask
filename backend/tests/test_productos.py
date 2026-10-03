def test_crear_y_listar_producto(client):
    response = client.post(
        "/api/productos",
        json={
            "nombre": "Producto de prueba",
            "descripcion": "Descripción de prueba",
            "precio": 100,
            "stock": 5,
            "activo": True,
        },
    )

    assert response.status_code == 201
    assert response.json["nombre"] == "Producto de prueba"

    response = client.get("/api/productos")

    assert response.status_code == 200
    assert len(response.json) == 1