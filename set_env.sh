#!/bin/bash

# Get a new JWT token
TOKEN=$(curl -X POST http://127.0.0.1:8080/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username": "admin"}' | jq -r .access_token)

# Export it as an environment variable
export JWT_TOKEN="$TOKEN"

echo "JWT Token has been set!"
