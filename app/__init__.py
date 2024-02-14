import logging
import os
from logging.config import dictConfig

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.settings.defaults import LOG_FILE_PATH, ERROR_LOG_FILE_PATH


db = SQLAlchemy()


def create_application(settings=None):
    raven_logger = logging.getLogger('raven.base.Client')
    raven_logger.setLevel(logging.CRITICAL)
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s][%(levelname)s][%(process)s][%(filename)s:%(lineno)d] %(message)s',
        }},
        'handlers': {
            'default': {
                'class': 'logging.StreamHandler',
                'formatter': 'default'
            },
            'file': {
                'formatter': 'default',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': LOG_FILE_PATH,
                'when': 'midnight'
            },
            'error': {
                'formatter': 'default',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'level': 'ERROR',
                'filename': ERROR_LOG_FILE_PATH,
                'when': 'midnight'
            }
        },
        'root': {
            'level': 'INFO',
            'handlers': ['default', 'file', 'error']
        }
    })

    app = Flask('app')
    app.config.from_object('app.settings.defaults')

    if os.environ.get('SETTINGS_MODULE'):
        app.config.from_object(os.environ.get('SETTINGS_MODULE'))

    if settings is not None:
        if isinstance(settings, dict):
            app.config.update(settings)
        else:
            app.config.from_object(settings)

    def init_mysql_db(app, db):
        db.init_app(app)

    init_mysql_db(app, db)

    # Register blueprints
    from app.api import api
    app.register_blueprint(api)

    return app