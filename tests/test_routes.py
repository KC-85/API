from flask_jwt_extended import create_access_token

def test_get_resources(client, auth_headers):
    """ Test fetching resources (Requires authentication) """
    response = client.get("/resources/tasks", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json, list)  # Should return a list

def test_add_resource(client, auth_headers):
    """ Test adding a resource (Admin Only) """
    response = client.post(
        "/resources/tasks",
        headers=auth_headers,
        json={"name": "Test Task", "status": "Pending"}
    )
    assert response.status_code == 201
    assert "id" in response.json

def test_delete_resource(client, auth_headers):
    """ Test deleting a resource (Admin Only) """
    response = client.delete("/resources/tasks/1", headers=auth_headers)
    assert response.status_code in [200, 404]  # Either deleted or already missing
