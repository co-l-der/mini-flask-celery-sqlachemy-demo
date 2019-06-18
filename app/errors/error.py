#!/usr/bin/env python
# encoding: utf-8
__author__ = "han"


class BaseRestfulException(Exception):

    def __init__(self, message, code):
        super().__init__()
        self.message = message
        self.code = code

    def to_dict(self):
        rv = dict()
        rv["message"] = self.message
        rv["code"] = self.code

        return rv


class InvalidParameter(BaseRestfulException):

    _code = 1001
    message = "invalid parameter"

    def __init__(self, message=None):
        if message:
            self.message = message
        super().__init__(self.message, self._code)
