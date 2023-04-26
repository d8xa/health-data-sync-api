import json
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash

auth = HTTPBasicAuth(scheme='Bearer')

def load_credentials():
    """Load credentials from a JSON file."""

    with open('credentials.json', 'r') as file: 
        return json.load(file)

credentials = load_credentials()

@auth.verify_password
def verify_password(username, password):
    """Verify the username and password provided by the user."""

    if username in credentials:
        stored_password = credentials[username]
        return check_password_hash(stored_password, password)
    return False