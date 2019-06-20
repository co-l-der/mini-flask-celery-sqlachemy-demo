#!/usr/bin/env python
# encoding: utf-8
from flask import Flask
from flask_cors import CORS

from app.model.schema import db

__author__ = "han"


def create_app(config="../config/config.py"):

    app = Flask(__name__)
    # 设置为允许跨域请求
    CORS(app, resources={r"/cat/*": {"origins": "*"}}, supports_credentials=True)
    app.config.from_pyfile(config)
    register_plugin(app)

    return app


def register_blueprint(app):
    from app.restful import bp, init
    app.register_blueprint(bp, url_prefix="/cat")
    init(app)


def register_plugin(app):
    db.init_app(app)
    db.create_all(app=app)
