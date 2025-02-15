import sys
import os

# Ensure the `app/` folder is in the system path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app

# Create an instance of the Flask app
app = create_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=app.config["DEBUG"])
