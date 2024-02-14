import celery
from celery.signals import worker_ready
from celery import shared_task

from app import db
from app.utils.method import METHOD


class Task(celery.Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r}'.format(task_id, exc))

    def on_success(self, retval, task_id, args, kwargs):
        pass

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        pass


@worker_ready.connect()
def on_worker_init(**_):
    pass


@shared_task
def db_sync(message: dict):
    session = db.sessionmaker(bind=db.create_engine(message['url'], engine_opts={}))
    session = session()
    object = globals()[message['instance']]
    try:
        if message['method'] != METHOD.DELETE.name:
            session.add(object(**message['body']))
            session.commit()
        else:
            session.delete(object(**message['body']))
            session.commit()
    except Exception as e:
        print(e)
    return {"status":True}
