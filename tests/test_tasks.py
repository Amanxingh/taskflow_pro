def test_health_check(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_and_get_task(client):
    created = client.post("/api/v1/tasks", json={
        "title": "Learn Docker",
        "description": "Build and run a container",
        "priority": "high"
    })
    assert created.status_code == 201
    task_id = created.json()["id"]

    fetched = client.get(f"/api/v1/tasks/{task_id}")
    assert fetched.status_code == 200
    assert fetched.json()["title"] == "Learn Docker"
    assert fetched.json()["completed"] is False


def test_update_and_delete_task(client):
    created = client.post("/api/v1/tasks", json={"title": "Practice Git"})
    task_id = created.json()["id"]

    updated = client.patch(f"/api/v1/tasks/{task_id}", json={"completed": True})
    assert updated.status_code == 200
    assert updated.json()["completed"] is True

    deleted = client.delete(f"/api/v1/tasks/{task_id}")
    assert deleted.status_code == 204
    assert client.get(f"/api/v1/tasks/{task_id}").status_code == 404


def test_validation_rejects_empty_title(client):
    response = client.post("/api/v1/tasks", json={"title": ""})
    assert response.status_code == 422
