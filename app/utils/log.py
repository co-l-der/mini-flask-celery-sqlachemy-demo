#!/usr/bin/env python
# encoding: utf-8
import logging
import os
import time
from datetime import datetime, date, timedelta

__author__ = "han"


class RestLogger(logging.Logger):

    FORMAT = "%(message)s"
    SUFFIX = "%Y%m%d_error.log"

    def __init__(self, name="flask_error"):
        logging.Logger.__init__(self, name)
        self.log_path = ""

    def init(self, log_path):
        self.log_path = log_path
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        self.rollover()

    def rollover(self):
        self.handlers = []
        filename = os.path.join(self.log_path, datetime.now().strftime(self.SUFFIX))
        handler = logging.FileHandler(filename)
        self.addHandler(handler)
        tomorrow = date.today() + timedelta(days=1)
        self.rolloverAt = datetime.strptime(str(tomorrow), "%Y-%m-%d")

    def record(self, data):
        t = int(time.time())
        dt = datetime.fromtimestamp(t)
        dt_str = dt.strftime("%Y-%m-%d %H:%M:%S")
        msg = "[{dt_str}, {data}]".format(dt_str=dt_str, data=data)
        if datetime.now() > self.rolloverAt:
            logging.Logger.info(self, msg)
