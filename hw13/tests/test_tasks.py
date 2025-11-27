def get_token_rw(client):
    client.post("/auth/register", json={
        "username": "taskuser",
        "password": "123",
        "is_read_only": False
    })
    res = client.post("/auth/login", json={"username": "taskuser", "password": "123"})
    return res.json()["token"]


def test_load_csv_task_start(client, tmp_path):
    token = get_token_rw(client)

    # создаём временный CSV
    csv_file = tmp_path / "students.csv"
    csv_file.write_text(
        "name,faculty,course\n"
        "Tom,IT,1\n"
        "Jerry,Math,2\n"
    )

    response = client.post(
        "/tasks/load_csv",
        params={"file_path": str(csv_file)},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "started"


def test_delete_students_task_start(client):
    token = get_token_rw(client)

    response = client.post(
        "/tasks/delete_students",
        json=[1, 2, 3],
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["task"] == "delete_students"
