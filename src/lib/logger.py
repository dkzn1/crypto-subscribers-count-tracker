from typing import Union
from datetime import datetime
import logging
from sqlalchemy.orm import Session
from sqlalchemy.engine.base import Engine

from db.db import db_singleton as db
from models.log_entry import LogEntry


class Logger:
    """
    Logger class for logging messages to both the console and a database.

    This class initializes a logger with customizable logging levels and formats.
    It can log messages of different severity levels, including success, warning, error, and critical.

    Args:
        db (Database): An instance of the Database class for database operations.
        name (str): The name of the logger.
        level (str, optional): The logging level for the logger. Default is 'info'.

    Attributes:
        __logger (Logger): The logger object configured for logging.

    Usage:
        To create an instance of the Logger class and log messages, use the methods like success, warn, error, and critical.
    """

    __default_level: str = 'info'

    def __init__(self, name: str, level: str = __default_level) -> None:
        """
        Initialize the Logger class.

        Initializes the logger object with a specified name and logging level.
        It also configures logging to both the console and a database.

        Args:
            name (str): The name of the logger.
            level (str, optional): The logging level for the logger. Default is 'info'.
        """
        levels = {
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warn': logging.WARN,
            'error': logging.ERROR,
            'critical': logging.CRITICAL,
        }

        logging.basicConfig(level=levels[level], format='%(levelname)s - %(asctime)s - %(name)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        logger = logging.getLogger(name)
        logger.propagate = False

        formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(name)s - %(message)s', '%Y-%m-%d %H:%M:%S')

        handler = logging.StreamHandler()
        handler.setLevel(levels['debug'])
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        db_handler = DatabaseHandler(db.engine)
        db_handler.setLevel(levels[level])
        db_handler.setFormatter(formatter)
        logger.addHandler(db_handler)

        self.__logger = logger

    #
    #
    #

    def success(self, message: Union[str, bool] = False) -> None:
        """
        Log a success message upon succesful fetch and save operation.

        Logs a success message to the logger.

        Args:
            message (Union[str, bool], optional): The success message to log. If not provided, a default message is used.
        """

        default = 'Succesfully retrieved and saved new data.'
        log = message if message else default

        self.__logger.info(log)

    #
    #
    #

    def warn(self, message: str) -> None:
        """
        Log a warning message with some predefined messages for failed fetch/scrape operations.

        Args:
            message (str): The warning message to log.
        """
        types = {'fetch_failure': 'Failed to fetch data after 5 attempts.', 'insufficient': 'Data is insufficient. Failed to fetch after several attempts.'}

        log = types[message] if message in types else message

        self.__logger.warn(log)

    #
    #
    #

    def error(self, message) -> None:
        """
        Logs an error message to the logger.

        Args:
            message (str): The error message to log.
        """
        self.__logger.error(message)

    #
    #
    #

    def critical(self, message: str) -> None:
        """
        Logs a critical message to the logger.

        Args:
            message (str): The critical message to log.
        """
        self.__logger.critical(message)


#


class DatabaseHandler(logging.Handler):
    """
    Custom Logging Handler for Database Integration.

    This custom logging handler logs messages to a database using SQLAlchemy. It is used with the custom logger
    created by the `create_logger` function.

    Args:
        engine: The SQLAlchemy database engine to connect to the database.

    Example:
        db_handler = DatabaseHandler(db.engine)
        logger.addHandler(db_handler)

    """

    def __init__(self, engine: Engine):
        super().__init__()
        self.__engine = engine

    def emit(self, record: logging.LogRecord):
        """
        Emit a Log Record to the Database.

        This method is called to handle log records and log them to the database.

        Args:
            record (LogRecord): The log record to be logged to the database.

        """
        log_entry = LogEntry(timestamp=datetime.fromtimestamp(record.created), level=record.levelname, name=record.name, message=record.getMessage())

        with Session(self.__engine) as session:
            try:
                session.add(log_entry)
                session.expire_on_commit = False
                session.commit()

            except Exception as e:
                logging.error(msg=str(e))
                session.rollback()
