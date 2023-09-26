from typing import Callable

from lib.base_classes.service_coordinator import ServiceCoordinator

from coin_subscribers_monitor.sub_tracker.sub_tracker_db_layer import SubTrackerDBLayer
from coin_subscribers_monitor.subscribers_monitor_config import SubscribersMonitorConfig

from coin_subscribers_monitor.sub_tracker.sub_tracker_data_formatter import SubTrackerDataFormatter
from coin_subscribers_monitor.sub_tracker.sub_tracker_data_finder import SubTrackerDataFinder

from db.db import Database
from lib.twitter_api import TwitterAPI


class SubTrackerCoordinator(ServiceCoordinator):
    """
    SubTrackerCoordinator is responsible for coordinating operations related to tracking social media subscribers of coins.

    Attributes:
        db (SubTrackerDBOperations): An instance of SubTrackerDBOperations for database operations.
        config (SubscribersMonitorConfig): An instance of SubscribersMonitorConfig for configuration settings.
        formatter (SubTrackerFormatter): An instance of SubTrackerFormatter for data formatting.
        finder (SubTrackerFinder): An instance of SubTrackerFinder for data finding operations.
        twitter (TwitterAPI): An instance of TwitterAPI for Twitter-related operations.
        scrape (Callable): A callable function for scraping data from a URL.
        fetch (Callable): A callable function for fetching data from an external source.
        _routine_interval_sec (int): The interval in seconds for running routines.
        _task (None): A placeholder for task-related data (if needed).

    Methods:
        __init__(self, database: Database, twitter_api: TwitterAPI, scrape: Callable, fetch: Callable) -> None:
            Constructor for initializing the SubtrackerCoordinator.

    """

    def __init__(self, database: Database, twitter_api: TwitterAPI, scrape: Callable, fetch: Callable) -> None:
        """
        Constructor for initializing the SubtrackerCoordinator.

        Args:
            database (Database): An instance of the Database class for database operations.
            formatter: An instance of the DataFormatter class.
            twitter_api (TwitterAPI): An instance of TwitterAPI for Twitter-related operations.
            scrape (Callable): A callable function for scraping data from a URL.
            fetch (Callable): A callable function for fetching data from an external source.
        """
        self.db = SubTrackerDBLayer(database)
        self.config = SubscribersMonitorConfig()

        self.finder = SubTrackerDataFinder()
        self.formatter = SubTrackerDataFormatter()

        self.twitter = twitter_api

        self.scrape = scrape
        self.fetch = fetch

        self._routine_interval_sec = self.config.routine_intervals_hours['24 hours'] * 360

        self._task = None
