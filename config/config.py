#!/usr/bin/env python
# encoding: utf-8
import os

__author__ = "han"


DEBUG = False
APP_PATH = "./"

# log保存位置
REST_LOG = APP_PATH + "/log/restful"

# celery配置
BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/1"
CELERY_IMPORTS = (
    "app.tasks.celery_task"
)
# 并发量
CELERYD_CONCURRENCY = 2

# 关系型数据库配置，此处使用sqlite
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.abspath(APP_PATH+"/database/demo.db")
