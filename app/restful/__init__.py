#!/usr/bin/env python
# encoding: utf-8
import traceback

from flask import Blueprint, request
from flask_restplus import Api

from app.errors.error import InvalidParameter
from app.utils.log import RestLogger

__author__ = "han"

bp = Blueprint("restful", __name__)
rest = Api(bp)
rest_logger = RestLogger()


def init(app):
    rest_log = app.config.get("REST_LOG", "")
    rest_logger.init(rest_log)


@rest.errorhandler(InvalidParameter)
# @rest.errorhandler(可在此处添加其它异常类)
def handle_exception(error):
    response = error.to_dict()
    tb = traceback.format_exc().splitlines()
    rest_logger.record("%s %s \n %s" % (request.remote_addr, request.full_path, "\n".join(tb[-3:])))

    return response, 200


@rest.errorhandler
def handle_unkown_exception(error):
    """
    作用：捕获未知异常
    :param error:
    :return:
    """
    if hasattr(error, "code"):
        code = error.code
        message = str(error)
    else:
        code = 500
        message = "Internal Server Error"
    tb = traceback.format_exc()
    rest_logger.record("%s %s \n %s" % (request.remote_addr, request.full_path, "\n".join(tb[-3:])))

    return dict(message=message, code=code), 200


# 防止循环引入
from app.restful import view

