from flask import Flask
from app.config import config


def create_app(environment='production'):

    # Create the Flask app instance
    app = Flask(__name__) 

    if environment == 'production':
        import logging
        gunicorn_error_logger = logging.getLogger('gunicorn.debug')
        app.logger.handlers.extend(gunicorn_error_logger.handlers)
        app.logger.setLevel(gunicorn_error_logger.level)
    
    # Load configuration based on the specified environment
    app.config.from_object(config[environment])

    # Register blueprints or routes
    from app.views import api
    app.register_blueprint(api.bp)

    return app