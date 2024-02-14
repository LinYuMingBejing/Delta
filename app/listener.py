from celery import Celery as BaseCelery
import raven
from raven.contrib.celery import register_signal, register_logger_signal
import os

from settings.defaults import CELERY_BROKER_URL


class Celery(BaseCelery):
    def on_configure(self):
        client = raven.Client(os.environ.get('SENTRY_DSN'))
        register_logger_signal(client)
        register_signal(client)


def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=CELERY_BROKER_URL
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.test_request_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    celery.autodiscover_tasks([app.name], related_name='tasks')
    return celery

import app

celery = make_celery(app.create_application())
task = celery.task

__all__ = ('task',)
