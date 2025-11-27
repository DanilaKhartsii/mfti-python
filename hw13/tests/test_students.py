def get_token(client):
    client.post("/auth/register", json={
        "username": "studentuser",
        "password": "123",
        "is_read_only": False
    })
    res = client.post("/auth/login", json={
        "username": "studentuser",
        "password": "123"
    })
    return res.json()["token"]


def test_create_student_ok(client):
    token = get_token(client)
    response = client.post(
        "/students/",
        json={"name": "Alice", "faculty": "IT", "course": 2},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Alice"


def test_create_student_no_token(client):
    response = client.post(
        "/students/",
        json={"name": "Bob", "faculty": "Math", "course": 1}
    )
    assert response.status_code == 401


def test_get_students(client):
    token = get_token(client)
    response = client.get("/students/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_single_student(client):
    token = get_token(client)

    create = client.post(
        "/students/",
        json={"name": "John", "faculty": "CS", "course": 3},
        headers={"Authorization": f"Bearer {token}"}
    )
    student_id = create.json()["id"]

    response = client.get(f"/students/{student_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["id"] == student_id
