import pytest
from jsonschema.exceptions import ValidationError
from app.core.validation import UploadJSONValidator
from app.core.upload import validate_json
from .utils import make_fake_data


@pytest.mark.parametrize('validate', [
    UploadJSONValidator().validate,
    validate_json,
])
class TestUploadJsonValidation:

    @pytest.fixture(autouse=True)
    def setup(self, validate):
        self.validate = validate

    def test_valid(self):
        data = make_fake_data()
        try:
            self.validate(data)
        except ValidationError as e:
            assert False, str(e)

    def test_invalid_empty(self):
        with pytest.raises(ValidationError):
            self.validate({})
    
    def test_invalid_empty_data(self):
        with pytest.raises(ValidationError):
            self.validate({'data': {}})