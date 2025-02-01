import time
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

def test_update_resource(client, auth_headers):
    """ Test updating an existing resource (Admin Only) """
    # Add a resource first
    client.post(
        "/resources/tasks",
        headers=auth_headers,
        json={"name": "Initial Task", "status": "Pending"}
    )

    # Update the resource
    response = client.put(
        "/resources/tasks/1",
        headers=auth_headers,
        json={"name": "Updated Task", "status": "Completed"}
    )
    assert response.status_code == 200
    assert response.json == {"id": 1, "name": "Updated Task", "status": "Completed"}

def test_update_resource_not_found(client, auth_headers):
    """ Test updating a non-existing resource (Should return 404) """
    response = client.put(
        "/resources/tasks/999",
        headers=auth_headers,
        json={"name": "Non-existent Task", "status": "Done"}
    )
    assert response.status_code == 404
    assert "error" in response.json

def test_update_rate_limit(client, auth_headers):
    """ Test that update requests are limited to 3 per minute """
    for _ in range(3):
        response = client.put(
            "/resources/tasks/1",
            headers=auth_headers,
            json={"name": "Rate Limit Test", "status": "Ongoing"}
        )
        assert response.status_code == 200  # Should succeed

    # Fourth request should fail due to rate limit
    response = client.put(
        "/resources/tasks/1",
        headers=auth_headers,
        json={"name": "Exceeding Rate Limit", "status": "Failed"}
    )
    assert response.status_code == 429  # Too Many Requests
    assert "Rate limit exceeded" in response.json["error"]

    # Wait 60 seconds before making another request
    time.sleep(60)
    
    # Now it should succeed again
    response = client.put(
        "/resources/tasks/1",
        headers=auth_headers,
        json={"name": "After Rate Limit Reset", "status": "Resumed"}
    )
    assert response.status_code == 200

def test_delete_resource(client, auth_headers):
    """ Test deleting a resource (Admin Only) """
    response = client.delete("/resources/tasks/1", headers=auth_headers)
    assert response.status_code in [200, 404]  # Either deleted or already missing
