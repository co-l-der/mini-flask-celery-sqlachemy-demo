#!/usr/bin/env python
# encoding: utf-8
from flask import jsonify
from flask_restplus import Resource

from app.errors.error import InvalidParameter
from app.restful import rest as api
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

        ret_dict = dict(id=args.get("id"), name=args.get("name"), gender=args.get("gender", ""))

        return jsonify({"code": 0, "data": ret_dict})
