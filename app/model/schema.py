#!/usr/bin/env python
# encoding: utf-8
from contextlib import contextmanager
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Integer, Column, String

__author__ = "han"


class SQLAlchemy(_SQLAlchemy):

    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.roolback()
            raise e


db = SQLAlchemy(query_class=BaseQuery)


# 数据库基类
class Base(db.Model):
    # 不创建base表
    __abstract__ = True

    create_time = Column("create_time", Integer, default=0)
    update_time = Column("update_time", Integer, default=0)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())
        self.update_time = int(datetime.now().timestamp())

    # 如果字典中有和Model中(除id外)相同名的key, 则自动赋值
    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != "id":
                setattr(self, key, value)

    # orm对象转换成dict
    def to_dict(self):
        result = {}
        for key in self.__mapper__.c.keys():
            if getattr(self, key) is not None and key != "id":
                result["key"] = str(getattr(self, key))

        return result

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    @property
    def update_datetime(self):
        if self.update_time:
            return datetime.fromtimestamp(self.update_time)
        else:
            return None


class CeleryTaskModel(Base):

    __tablename__ = "celery_task"

    id = Column("id", Integer, primary_key=True)
    task_id = Column("task_id", String)
    task_detail = Column("task_detail", String)

    def save_celery_task(self, args, result):
        """
        功能：存储celery_task
        :param args:
        :param result:
        :return:
        """
        args["task_detail"] = str(args)
        args["task_id"] = result.id

        with db.auto_commit():
            self.set_attrs(attrs_dict=args)
            self.create_time = int(datetime.now().timestamp())
            self.update_time = int(datetime.now().timestamp())

