def test_register(client):
    """ Test user registration """
    response = client.post("/auth/register", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 201
    assert response.json == {"message": "User registered successfully"}  # Fix assertion to match response

def test_login(client):
    """ Test user login """
    client.post("/auth/register", json={"username": "testuser", "password": "testpass"})  # Register user first
    response = client.post("/auth/login", json={"username": "testuser"})
    assert response.status_code == 200
    assert "access_token" in response.json

def test_invalid_login(client):
    """ Test login with non-existent user """
    response = client.post("/auth/login", json={"username": "nonexistent"})
    assert response.status_code == 401
    assert response.json == {"error": "Invalid credentials"}
