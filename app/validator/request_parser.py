#!/usr/bin/env python
# encoding: utf-8
from flask import request
from flask_restplus.reqparse import RequestParser, Argument
from werkzeug.exceptions import BadRequest

from app.errors.error import InvalidParameter

__author__ = "han"


class BaseRequestParser(RequestParser):

    def __init__(self, *args, **kwargs):
        self._message = ""
        super().__init__(*args, **kwargs)

    def parse_args(self, req=None, strict=False):

        if req is None:
            req = request

        result = self.result_class()

        req.unparsed_arguments = dict(self.argument_class("").source(req)) if strict else {}
        errors = {}
        source = None
        for arg in self.args:
            try:
                if not source:
                    source = arg.source(req)
            except BadRequest:
                raise InvalidParameter(message="failed to decode json object")

            try:
                value, found = arg.parse(req)
                if isinstance(value, ValueError):
                    errors.update(found)
                    found = None
                if found or arg.store_missing:
                    result[arg.dest or arg.name] = value
            except Exception:
                raise InvalidParameter("%s validation failed" % arg.name)

        if errors:
            raise InvalidParameter(str(errors))

        if strict and req.unparsed_arguments:
            arguments = ", ".join(req.unparsed_arguments.keys())
            msg = "Unknown arguments: {0}".format(arguments)
            raise InvalidParameter(message=msg)

        return result
