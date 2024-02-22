import os

# sqlalchemy
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI','mysql+pymysql://root:root@localhost:3306/demo?charset=utf8mb4')
SQLALCHEMY_BINDS = {
    'external_database': os.environ.get('EXTERNAL_DATABASE_URI'),
    'internal_database': os.environ.get('INTERNAL_DATABASE_URI')
}
SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', True)

# Celery
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')
CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = 'Asia/Taipei'
CELERYD_LOG_FORMAT = '%(asctime)s stdout F [%(levelname)s]%(message)s}'
CELERY_ENABLE_UTC = True
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
# CELERY_MESSAGE_COMPRESSION = 'json'
CELERY_TASK_RESULT_EXPIRES = 600
CELERY_ACCEPT_CONTENT = (os.environ.get('CELERY_ACCEPT_CONTENT') or ' '.join(['json'])).split()

LOG_FILE_PATH = os.environ.get('LOG_FILE_PATH') or 'demo.log'
ERROR_LOG_FILE_PATH = os.environ.get('ERROR_LOG_FILE_PATH') or 'demo.log'
