from typing import Callable

from lib.base_classes.service_coordinator import ServiceCoordinator

from coin_data_manager.social_links.social_links_data_validator import SocialLinksDataValidator
from coin_data_manager.social_links.social_links_data_formatter import SocialLinksDataFormatter
from coin_data_manager.social_links.social_links_data_finder import SocialLinksDataFinder

from coin_data_manager.social_links.social_links_db_layer import SocialLinksDBLayer
from coin_data_manager.social_links.social_links_routine import SocialLinksRoutine
from coin_data_manager.social_links.social_links_config import SocialLinksConfig

from db.db import Database


class SocialLinksCoordinator(ServiceCoordinator):
    """
    Social Links Coordinator for managing social links data.

    This class is responsible for coordinating social links-related tasks such as  including scraping, processing, and storing data.

    Attributes:
        db (SocialLinksDBOperations): An instance of SocialLinksDBOperations for database operations.
        config (SocialLinksConfig): An instance of SocialLinksConfig for configuration settings.
        formatter (SocialLinksDataProcessor): An instance of SocialLinksDataFormatter for data formatting.
        finder (SocialLinksDataFinder): An instance of SocialLinksDataFinder for data finding data.
        validator (SocialLinksDataValidator): An instance of SocialLinksDataValidator for data validation.
        routines (dict[str, SocialLinksRoutine]): A dictionary mapping routine names to their corresponding routine instances.
        scrape (Callable): A Callable function for scraping data from a URL.
        _routine_interval_sec (int): The interval in seconds between routine executions.
        _task (None): A placeholder for the asynchronous task associated with the routine.

    Methods:
        __init__: Initializes the SocialLinksCoordinator instance.
    """

    def __init__(self, database: Database, scrape_url: Callable) -> None:
        """
        Constructor for initializing the SocialLinksCoordinator.

        Args:
            database (Database): An instance of the Database class for database operations.
            scrape_url (Callable): A Callable function for scraping data from a URL.
        """
        self.db = SocialLinksDBLayer(database)
        self.config = SocialLinksConfig()

        self.formatter = SocialLinksDataFormatter()
        self.finder = SocialLinksDataFinder()
        self.validator = SocialLinksDataValidator()

        self.scrape = scrape_url

        self._routine_interval_sec = self.config.routine_intervals_hours['12 min'] * 360

        self._task = None

        self.routines = {"SocialLinksRoutine": SocialLinksRoutine(service=self)}
