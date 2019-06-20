#!/usr/bin/env python
# encoding: utf-8
from flask import jsonify
from flask_restplus import Resource

from app.errors.error import InvalidParameter, CeleryTaskException
from app.model.schema import CeleryTaskModel
from app.restful import rest as api
from app.tasks.celery_task import execute_time_consuming_operation, get_task_status
from app.validator import request_parser

__author__ = "han"


@api.route("/detail")
class DetailResource(Resource):

    parser = request_parser.BaseRequestParser()
    parser.add_argument("id", type=int, required=True, location="json")
    parser.add_argument("name", type=str, required=True, location="json")
    parser.add_argument("gender", type=str, required=False, location="json")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self):

        try:
            args = self.parser.parse_args()
        except InvalidParameter as e:
            raise InvalidParameter(message=e.message)

        try:
            result = execute_time_consuming_operation.delay(**dict(args))
        except Exception:
            raise CeleryTaskException()

        celery_task_model = CeleryTaskModel()
        celery_task_model.save_celery_task(args, result)
        ret_dict = dict(task_id=result.id)

        return jsonify({"code": 0, "data": ret_dict})


@api.route("/status")
class TaskStatusResource(Resource):
    parser = request_parser.BaseRequestParser()
    parser.add_argument("task_id", type=str, required=True, location="json")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self):

        try:
            args = self.parser.parse_args()
        except InvalidParameter as e:
            raise InvalidParameter(message=e.message)
        # 获取任务状态
        try:
            status = get_task_status(args.get("task_id"))
        except Exception:
            raise CeleryTaskException()

        ret_dict = dict(status=status)

        return jsonify({"code": 0, "data": ret_dict})
