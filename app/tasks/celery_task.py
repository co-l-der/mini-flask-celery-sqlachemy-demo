#!/usr/bin/env python
# encoding: utf-8
import time

from celery import Celery

from app import create_app

__author__ = "han"


def make_celery(app):

    celery = Celery(app.import_name)
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


flask_app = create_app("../config/config.py")
celery = make_celery(flask_app)


@celery.task()
def execute_time_consuming_operation(*args, **kwargs):
    print(args, kwargs)
    time.sleep(180)
    return args, kwargs


def get_task_status(task_id):
    res = celery.AsyncResult(task_id)
    return res.state
