from typing import Callable

from lib.base_classes.service_coordinator import ServiceCoordinator

from coin_subscribers_monitor.subscribers_monitor_config import SubscribersMonitorConfig

from coin_subscribers_monitor.sub_tracker.sub_tracker_coordinator import SubTrackerCoordinator
from coin_subscribers_monitor.trend_monitor.trend_monitor_coordinator import TrendMonitorCoordinator

from coin_subscribers_monitor.sub_tracker.sub_tracker_routine import SubTrackerRoutine
from coin_subscribers_monitor.trend_monitor.trend_monitor_routine import TrendMonitorRoutine

from lib.twitter_api import TwitterAPI


from db.db import Database


class SubscribersMonitorCoordinator(ServiceCoordinator):
    """
    SubscribersMonitorCoordinator is a coordinator class responsible for managing and scheduling routines for
    subscriber monitoring tasks, such as tracking social media subscribers and trends.

    Composes routines for 2 sub coordinators, SubTrackerCoordinator and TrendMonitorCoordinator.

    Args:
        database (Database): An instance of the Database class for database operations.
        twitter_api (TwitterAPI): An instance of the TwitterAPI class for interacting with the Twitter API.
        scrape (Callable): A callable function for web scraping operations.
        fetch (Callable): A callable function for fetching data from web sources.
    """

    def __init__(self, database: Database, twitter_api: TwitterAPI, scrape: Callable, fetch: Callable) -> None:
        """
        Initializes a new instance of SubscribersMonitorCoordinator.
        """
        sub_tracker = SubTrackerCoordinator(database, twitter_api, scrape, fetch)
        trend_monitor = TrendMonitorCoordinator(database)

        self.config = SubscribersMonitorConfig()

        self.routines = {"SubTrackerRoutine": SubTrackerRoutine(service=sub_tracker), "TrendMonitorRoutine": TrendMonitorRoutine(service=trend_monitor)}

        self._routine_interval_sec = self.config.routine_intervals_hours['15 min'] * 360
