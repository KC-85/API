import sys
import os

# Add the root project directory to `sys.path`
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Debugging: Print current paths
print("Current working directory:", os.getcwd())
print("Python path:", sys.path)

try:
    from app import create_app
    print("Successfully imported 'app'")
except ModuleNotFoundError as e:
    print("ERROR: Could not import 'app'", e)

# Create an instance of the Flask app
app = create_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=app.config["DEBUG"])
