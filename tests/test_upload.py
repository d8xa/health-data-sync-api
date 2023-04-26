from .setup import *
from .utils import make_fake_data
import json
from werkzeug.exceptions import RequestEntityTooLarge, BadRequest
from pathlib import Path
from app.core.upload import save_json, make_save_path
from datetime import datetime as dt
from flask import url_for

@pytest.fixture(autouse=True)
def setup(app_use_tmp_path):
    pass


class TestUploadRoute:

    @pytest.fixture(autouse=True)
    def setup(self, app_use_tmp_path):
        self.url = url_for('api.upload')

    def test_upload_valid_content(self, authenticated_client):
        data = make_fake_data()
        response = authenticated_client.post(self.url, json=data)
        assert response.status_code == 200
        assert response.json['message'] == 'Upload successful'

    def test_upload_exceeds_max_content_length(self, app, authenticated_client):
        max_length = app.config['MAX_CONTENT_LENGTH']
        data = make_fake_data()
        data['data']['extra_field'] = [
            x for x in range(max_length - len(json.dumps(data)))
        ]
        response = authenticated_client.post(self.url, json=data)
        assert response.status_code == RequestEntityTooLarge.code

    def test_upload_invalid_content_type(self, authenticated_client):
        data = 'test'
        response = authenticated_client.post(self.url, data=data)
        assert response.status_code == BadRequest.code
        assert "Only JSON requests are allowed" in response.json['message']

    def test_upload_invalid_json_schema(self, authenticated_client):
        data = {'data': {'field1': 'value1', 'field2': 'value2'}}
        response = authenticated_client.post('/api/upload', json=data)
        assert response.status_code == BadRequest.code
        assert response.json['error'] == "Validation Error"


class TestUploadFunction:

    def savepath(self, app):
        return make_save_path(app.config['UPLOAD_DIR'])

    def assert_json_received(self, data, p):
        assert p.parent.exists()
        assert p.exists()

        with p.open('r') as f:
            received = json.load(f)
        assert received == data

    def test_save_json(self, app, app_use_tmp_path):
        data = make_fake_data()
        p = self.savepath(app)
        save_json(data, app.config['UPLOAD_DIR'])
        self.assert_json_received(data ,p)

    def test_receive_json(self, app, app_use_tmp_path, authenticated_client):
        data = make_fake_data()
        p = self.savepath(app)
        resp = authenticated_client.post('/api/upload', json=data)
        assert resp.status_code == 200
        self.assert_json_received(data, p)