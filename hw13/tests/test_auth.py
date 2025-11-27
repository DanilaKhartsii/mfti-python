def test_register_user(client):
    response = client.post("/auth/register", json={
        "username": "testuser",
        "password": "123",
        "is_read_only": False
    })
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"


def test_login_user(client):
    client.post("/auth/register", json={
        "username": "loginuser",
        "password": "pass",
        "is_read_only": False
    })

    response = client.post("/auth/login", json={
        "username": "loginuser",
        "password": "pass"
    })
    assert response.status_code == 200
    assert "token" in response.json()


def test_protected_without_token(client):
    response = client.get("/students/")
    assert response.status_code == 401
