from flask import jsonify, make_response, url_for
from app.core.auth import auth
from .setup import *
from .utils import make_fake_data
from werkzeug.exceptions import Unauthorized


class TestLoginRequired:
    @auth.login_required
    def dummy_upload(self):
        return make_response(jsonify({"message": "Upload successful"}), 200)

    def test_valid(self, app):
        with app.test_request_context(headers=dummy_auth_header()):
            resp = self.dummy_upload()
            assert resp.status_code == 200

    def test_invalid(self, app):
        with app.test_request_context():
            resp = self.dummy_upload()
            assert resp.status_code == Unauthorized.code


class TestAuthentication:

    @pytest.fixture(autouse=True)
    def setup(self, app):
        with app.test_request_context(): # only needed for url_for
            self.url = url_for('api.upload')

    def test_call_no_auth(self, app):
        """Test a request without authentication"""
        with app.test_client() as client:
            response = client.post(self.url, json=make_fake_data())
            assert response.status_code == 401

    def test_call_valid_auth(self, app, app_use_tmp_path):
        """Test a request with valid authentication"""
        with app.test_client() as client:
            response = client.post(self.url, headers=dummy_auth_header(), json=make_fake_data())
            assert response.status_code == 200, response.data

    def test_call_invalid_auth(self, app):
        """Test a request with invalid authentication"""
        with app.test_client() as client:
            response = client.post(self.url, headers={'Authorization': 'Basic dXNlcjpwYXNzd29yZA=='}, json=make_fake_data())
            assert response.status_code == Unauthorized.code


class TestAuthenticatedClientFixture:
    def test(self, app_use_tmp_path, authenticated_client):
        """Test a request with valid authentication"""
        response = authenticated_client.post(url_for('api.upload'), json=make_fake_data())
        assert response.status_code == 200, response.data