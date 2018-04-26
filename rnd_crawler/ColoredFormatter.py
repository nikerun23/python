# -*- coding: UTF-8 -*-
import logging


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno == logging.WARNING:
            record.msg = '\033[93m%s\033[0m' % record.msg  # Yellow
        elif record.levelno == logging.ERROR:
            record.msg = '\033[91m%s\033[0m' % record.msg  # RED
        elif record.levelno == logging.DEBUG:
            record.msg = '\033[92m%s\033[0m' % record.msg  # Green
        elif record.levelno == logging.INFO:
            record.msg = '\033[99m%s\033[0m' % record.msg  # Default
        return logging.Formatter.format(self, record)


# Red = '\033[91m'
# Green = '\033[92m'
# Blue = '\033[94m'
# Cyan = '\033[96m'
# White = '\033[97m'
# Yellow = '\033[93m'
# Magenta = '\033[95m'
# Grey = '\033[90m'
# Black = '\033[90m'
# Default = '\033[99m'