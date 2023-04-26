import pytest
import base64
from app.app import create_app

@pytest.fixture
def app():
    app = create_app(environment='development')
    return app

@pytest.fixture
def app_use_tmp_path(app, tmp_path):
    """Use a temporary path for the UPLOAD_DIR"""

    with app.test_request_context():
        app.config['UPLOAD_DIR'] = str(tmp_path)
        yield

@pytest.fixture
def authenticated_client(app):
    with app.test_client() as client:
        client.environ_base['HTTP_AUTHORIZATION'] = dummy_auth_header()['Authorization']
        yield client

def dummy_auth_header():
    username = 'dummy-user'
    password = 'dummy-password'
    auth_header = 'Basic ' + base64.b64encode(f"{username}:{password}".encode()).decode()
    return {'Authorization': auth_header}