#!/usr/bin/env python
# encoding: utf-8
from app import create_app, register_blueprint

__author__ = "han"

app = create_app("../config/config.py")
register_blueprint(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
