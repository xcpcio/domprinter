import yaml
import logging
import os
import colorlog
from logging.handlers import RotatingFileHandler
from datetime import datetime

def read_config(dir: str="./config.yaml"):
    with open(dir) as file:
        return yaml.safe_load(file)

cur_path = os.path.dirname(os.path.realpath(__file__))  
log_path = os.path.join(os.path.dirname(cur_path), 'logs') 
if not os.path.exists(log_path): os.mkdir(log_path)

log_colors_config = {
    'DEBUG': 'white',
    'INFO': 'cyan',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}

default_formats = {
    'color_format': '%(log_color)s%(asctime)s-%(name)s-%(filename)s-[line:%(lineno)d]-%(levelname)s-[Log]: %(message)s',
    'log_format': '%(asctime)s-%(name)s-%(filename)s-[line:%(lineno)d]-%(levelname)s-[LoggerInfo]: %(message)s'
}


class Logger:

    def __init__(self):
        self.__now_time = datetime.now().strftime('%Y-%m-%d') 
        self.__all_log_path = os.path.join(log_path, self.__now_time + "-all" + ".log") 
        self.__error_log_path = os.path.join(log_path, self.__now_time + "-error" + ".log") 
        self.__logger = logging.getLogger() 
        self.__logger.setLevel(logging.DEBUG) 

    @staticmethod
    def __init_logger_handler(log_path):
        logger_handler = RotatingFileHandler(filename=log_path, maxBytes=1 * 1024 * 1024, backupCount=3, encoding='utf-8')
        return logger_handler

    @staticmethod
    def __init_console_handle():
        console_handle = colorlog.StreamHandler()
        return console_handle

    def __set_log_handler(self, logger_handler, level=logging.DEBUG):
        logger_handler.setLevel(level=level)
        self.__logger.addHandler(logger_handler)

    def __set_color_handle(self, console_handle):
        console_handle.setLevel(logging.DEBUG)
        self.__logger.addHandler(console_handle)

    @staticmethod
    def __set_color_formatter(console_handle, color_config):
        formatter = colorlog.ColoredFormatter(default_formats["color_format"], log_colors=color_config)
        console_handle.setFormatter(formatter)

    @staticmethod
    def __set_log_formatter(file_handler):
        formatter = logging.Formatter(default_formats["log_format"], datefmt='%a, %d %b %Y %H:%M:%S')
        file_handler.setFormatter(formatter)

    @staticmethod
    def __close_handler(file_handler):
        file_handler.close()

    def __console(self, level, message):
        all_logger_handler = self.__init_logger_handler(self.__all_log_path) 
        error_logger_handler = self.__init_logger_handler(self.__error_log_path)
        console_handle = self.__init_console_handle()

        self.__set_log_formatter(all_logger_handler)
        self.__set_log_formatter(error_logger_handler)
        self.__set_color_formatter(console_handle, log_colors_config)

        self.__set_log_handler(all_logger_handler) 
        self.__set_log_handler(error_logger_handler, level=logging.ERROR)
        self.__set_color_handle(console_handle)

        if level == 'info':
            self.__logger.info(message)
        elif level == 'debug':
            self.__logger.debug(message)
        elif level == 'warning':
            self.__logger.warning(message)
        elif level == 'error':
            self.__logger.error(message)
        elif level == 'critical':
            self.__logger.critical(message)

        self.__logger.removeHandler(all_logger_handler)
        self.__logger.removeHandler(error_logger_handler)
        self.__logger.removeHandler(console_handle)

        self.__close_handler(all_logger_handler)
        self.__close_handler(error_logger_handler)

    def debug(self, message):
        self.__console('debug', message)

    def info(self, message):
        self.__console('info', message)

    def warning(self, message):
        self.__console('warning', message)

    def error(self, message):
        self.__console('error', message)

    def critical(self, message):
        self.__console('critical', message)


