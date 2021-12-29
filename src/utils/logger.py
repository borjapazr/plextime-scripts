import logging
import logging.handlers
import os
import sys

import coloredlogs


class PlxLogger:
    __LEVEL = logging.INFO
    __LOG_FILE = "./log/records.log"
    __FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    @staticmethod
    def get_logger(service):
        logger = logging.getLogger(service)
        logger.setLevel(PlxLogger.__LEVEL)
        logger.addHandler(PlxLogger.__get_console_handler())
        logger.addHandler(PlxLogger.__get_file_handler())
        return logger

    @staticmethod
    def __get_console_handler():
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(coloredlogs.ColoredFormatter(PlxLogger.__FORMAT))
        console_handler.setLevel(PlxLogger.__LEVEL)
        return console_handler

    @staticmethod
    def __get_file_handler():
        os.makedirs(os.path.dirname(PlxLogger.__LOG_FILE), exist_ok=True)
        file_handler = logging.handlers.RotatingFileHandler(
            PlxLogger.__LOG_FILE,
            maxBytes=500000000,  # 500MB
            backupCount=10,
            encoding="utf-8",
        )
        file_handler.setFormatter(logging.Formatter(PlxLogger.__FORMAT))
        file_handler.setLevel(PlxLogger.__LEVEL)
        return file_handler
