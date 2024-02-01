import logging
import traceback
from django.conf import settings

# Global variable to determine if DEBUG mode is enabled
DEBUG = settings.DEBUG


class LogInfo(logging.Logger):
    def __init__(self, name):
        super().__init__(name)

    @staticmethod
    def configure_logger(logger_name):
        """
        Configure and return a logger with the specified name.
        Args:
            logger_name (str): The name of the logger.
        Returns:
            logging.Logger: The configured logger.
        """
        return logging.getLogger(logger_name)

    @staticmethod
    def print_to_console(msg):
        """
        Print the message to the console if DEBUG mode is enabled.
        Args:
            msg (str): The message to print.
        """
        if DEBUG:
            print(msg)

    @staticmethod
    def debug(msg, *args, **kwargs):
        """
        Log a DEBUG message.
        Args:
            msg (str): The log message.
            *args: Additional positional arguments for the logging method.
            **kwargs: Additional keyword arguments for the logging method.
        """
        logger = LogInfo.configure_logger('debug_logger')
        logger.debug(msg, *args, **kwargs)

    @staticmethod
    def info(msg, *args, **kwargs):
        """
        Log an INFO message.
        Args:
            msg (str): The log message.
            *args: Additional positional arguments for the logging method.
            **kwargs: Additional keyword arguments for the logging method.
        """
        logger = LogInfo.configure_logger('info_logger')
        logger.info(msg, *args, **kwargs)

    @staticmethod
    def error(msg, *args, **kwargs):
        """
        Log an ERROR message and print to the console in DEBUG mode.
        Args:
            msg (str): The log message.
            *args: Additional positional arguments for the logging method.
            **kwargs: Additional keyword arguments for the logging method.
        """
        logger = LogInfo.configure_logger('error_logger')
        LogInfo.print_to_console(msg)
        logger.error(msg, *args, **kwargs)

    @staticmethod
    def exception(msg, *args, **kwargs):
        """
        Log an ERROR message with an exception traceback and print to the console in DEBUG mode.
        Args:
            msg (str): The log message.
            *args: Additional positional arguments for the logging method.
            **kwargs: Additional keyword arguments for the logging method.
        """
        logger = LogInfo.configure_logger('error_logger')
        stack_trace = traceback.format_exc()
        LogInfo.print_to_console(f"{msg}\n{stack_trace}")
        logger.exception(msg, *args, **kwargs)

    @staticmethod
    def celery_log_info(msg, *args, **kwargs):
        """
        Log an INFO message for Celery-related logs.
        Args:
            msg (str): The log message.
            *args: Additional positional arguments for the logging method.
            **kwargs: Additional keyword arguments for the logging method.
        """
        logger = LogInfo.configure_logger('celery')
        logger.info(msg, *args, **kwargs)

    @staticmethod
    def email_log_info(msg, *args, **kwargs):
        """
        Log an INFO message for email-related logs.
        Args:
            msg (str): The log message.
            *args: Additional positional arguments for the logging method.
            **kwargs: Additional keyword arguments for the logging method.
        """
        logger = LogInfo.configure_logger('email')
        logger.info(msg, *args, **kwargs)
