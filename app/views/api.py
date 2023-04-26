from flask import Blueprint, jsonify, make_response, request
from flask import current_app as app
from ..core.auth import auth
from ..core.upload import save_json, validate_json
from werkzeug.exceptions import BadRequest, InternalServerError, RequestEntityTooLarge, HTTPException
from jsonschema.exceptions import ValidationError

bp = Blueprint("api", __name__, url_prefix="/api")

@bp.route("/upload", methods=["POST"], endpoint="upload")
@auth.login_required
def upload():
    """Upload a JSON file to the server."""

    validate_request()
    content = request.get_json(silent=False)
    validate_json(content)
    save_json(content, app.config['UPLOAD_DIR'])
    return make_response(jsonify({'message': 'Upload successful'}), 200)

def validate_request():
    if request.method != 'POST':
        raise BadRequest('Only POST requests are allowed')
    if not request.is_json:
        raise BadRequest('Only JSON requests are allowed')
    if int(request.headers.get('Content-Length', 0)) > request.max_content_length:
        raise RequestEntityTooLarge('Can not upload data larger than {} bytes'.format(request.max_content_length))

@bp.errorhandler(Exception)
def default_error_handler(error):
    if isinstance(error, HTTPException):
        # Handle HTTP exceptions with their specific error codes and descriptions
        response = {
            'error': error.name,
            'message': error.description
        }
        status_code = error.code
    elif isinstance(error, ValidationError):
        # Handle ValidationError with a specific error message
        response = {
            'error': 'Validation Error',
            'message': str(error)
        }
        status_code = BadRequest.code
    else:
        # Handle other exceptions with a generic error message
        response = {
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred'
        }
        status_code = InternalServerError.code
        app.logger.exception(error)

    return jsonify(response), status_code
