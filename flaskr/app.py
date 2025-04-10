'''
from flask import Flask
from flaskr.auth import bp as auth_bp  # Import the auth Blueprint

app = Flask(__name__)
print(app.url_map)  # Debug all routes
# Register the Blueprint
app.register_blueprint(auth_bp)

'''