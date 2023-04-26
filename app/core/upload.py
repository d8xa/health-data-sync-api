from .validation import UploadJSONValidator
from pathlib import Path
import json
from datetime import datetime as dt

UPLOAD_VALIDATOR = UploadJSONValidator()

def make_save_path(target_dir: str | Path):
    return (
        Path(target_dir)
        / 'json'
        / '{}.json'.format(dt.now().strftime('%Y-%m-%dT%H-%M'))
    )

def save_json(data: dict, target_dir: str | Path, *args):
    save_path = make_save_path(target_dir)
    save_path.parent.mkdir(exist_ok=True, parents=True)
    with save_path.open('w') as d:
        json.dump(data, d)

def validate_json(json_data):
    return UPLOAD_VALIDATOR.validate(json_data)