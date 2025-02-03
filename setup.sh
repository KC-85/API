#!/bin/bash

echo "🔄 Updating system and installing dependencies..."
sudo apt update && sudo apt install -y redis-server python3-pip

echo "🚀 Starting Redis server..."
redis-server --daemonize yes  # Starts Redis in the background

echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo "🧪 Running tests..."
pytest -v

echo "✅ Setup complete!"
