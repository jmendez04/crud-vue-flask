def test_crear_y_listar_cliente(client):
    response = client.post(
        "/api/clientes",
        json={
            "nombre": "Cliente de prueba",
            "correo": "prueba@example.com",
        },
    )

    assert response.status_code == 201
    assert response.json["nombre"] == "Cliente de prueba"

    response = client.get("/api/clientes")

    assert response.status_code == 200
    assert len(response.json) == 1