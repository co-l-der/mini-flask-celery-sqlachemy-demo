#!/usr/bin/env python
# encoding: utf-8
"""
用途：database migrate
使用命令：
1. python migrate.py db init
2. python migrate.py db migrate
3. python migrate.py db upgrade
"""
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import create_app, db

__author__ = "han"


app = create_app("../config/config.py")

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()