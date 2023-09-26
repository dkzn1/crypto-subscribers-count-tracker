from lib.base_classes.service_coordinator import ServiceCoordinator

from coin_subscribers_monitor.trend_monitor.trend_monitor_db_layer import TrendMonitorDBLayer
from coin_subscribers_monitor.subscribers_monitor_config import SubscribersMonitorConfig

from coin_subscribers_monitor.trend_monitor.trend_monitor_data_processor import TrendMonitorProcessor
from coin_subscribers_monitor.trend_monitor.trend_monitor_data_formatter import TrendMonitorFormatter

from db.db import Database


class TrendMonitorCoordinator(ServiceCoordinator):
    """
    TrendMonitorCoordinator class is responsible for coordinating the Trend Monitor service.

    Attributes:
        db (TrendMonitorDBOperations): An instance of TrendMonitorDBOperations for database operations.
        config (SubscribersMonitorConfig): An instance of SubscribersMonitorConfig for configuration settings.
        formatter (TrendMonitorFormatter): An instance of TrendMonitorFormatter for data formatting.
        processor (TrendMonitorProcessor): An instance of TrendMonitorProcessor for data finding operations.
        _routine_interval_sec (int): The interval in seconds for running routines.
        _task (None): A placeholder for task-related data (if needed).

    Methods:
        __init__(self, database: Database) -> None:
            Constructor for initializing the TrendMonitorCoordinator.
    """

    def __init__(self, database: Database) -> None:
        """
        Constructor for initializing the TrendMonitorCoordinator.

        Args:
            database (Database): An instance of the Database class for database operations.
        """
        self.db = TrendMonitorDBLayer(database)
        self.config = SubscribersMonitorConfig()

        self.processor = TrendMonitorProcessor()
        self.formatter = TrendMonitorFormatter()

        self._routine_interval_sec = self.config.routine_intervals_hours['24 hours'] * 360

        self._task = None
