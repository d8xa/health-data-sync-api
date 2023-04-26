import json
from pathlib import Path
from jsonschema import Draft201909Validator, RefResolver


def load_json(file_path: str | Path):
    with open(file_path, 'r') as f:
        return json.load(f)

def make_validator(main_schema_path: Path):
    """
    Creates a JSON validator for the main schema, using a custom RefResolver to register all referenced sub-schemas.
    """

    schema_files = list(main_schema_path.parent.iterdir())
    schemas = (
        load_json(file) for file in schema_files
        if file.suffix == '.json'
    )
    schema_store = {
        schema.get("$id", file.stem): schema 
        for schema,file in zip(schemas, schema_files)
    }
    schema = load_json(main_schema_path)
    resolver = RefResolver.from_schema(schema, store=schema_store)
    validator = Draft201909Validator(schema, resolver=resolver)
    return validator

class UploadJSONValidator():
    """Custom JSON validator for uploads."""

    def __new__(cls, *args, **kwargs):
        main_schema_path = Path(__file__).parent.parent / 'schemas' / 'main.json'
        return make_validator(main_schema_path)
        