from typing import Callable

from lib.base_classes.service_coordinator import ServiceCoordinator

from coin_data_manager.coingecko.coingecko_data_cleaner import CoingeckoDataCleaner
from coin_data_manager.coingecko.coingecko_data_formatter import CoingeckoDataFormatter
from coin_data_manager.coingecko.coingecko_data_finder import CoingeckoDataFinder

from coin_data_manager.coingecko.coingecko_endpoints import CoingeckoEndpoints
from coin_data_manager.coingecko.coingecko_config import CoingeckoConfig
from coin_data_manager.coingecko.coingecko_db_layer import CoingeckoDBLayer

from coin_data_manager.coingecko.coingecko_routines import coingecko_routines_factory

from db.db import Database


class CoingeckoCoordinator(ServiceCoordinator):
    """
    Coordinator class for managing CoinGecko-related routines.

    This class coordinates and manages various components and tasks related to the Coingecko API service.

    Attributes:
        db: An instance of CoingeckoDBOperations for database operations.
        config: An instance of CoingeckoConfig for configuration settings.
        endpoints: An instance of CoingeckoEndpoints for API endpoints.
        processor: An instance of CoingeckoDataProcessor for data processing methods.
        routines: An instance of CoingeckoRoutinesFactory for creating and managing routines.
        fetch: A Callable function for fetching data.
        scrape: A Callable function for scraping data.
        _routine_interval_sec:
        task: An asyncio.Task object representing the running routine task.

    Methods:
        __init__: Constructor for initializing the CoingeckoCoordinator.
    """

    def __init__(self, database: Database, fetch_json: Callable, scrape_url: Callable) -> None:
        """
        Constructor for initializing the CoingeckoCoordinator.

        Args:
            database: An instance of the Database class for database operations.
            fetch_json: A Callable function for fetching JSON data from APIs.
            scrape_url: A Callable function for scraping data from a URL.
        """
        self.db = CoingeckoDBLayer(database)

        cfg = CoingeckoConfig()

        self.endpoints = CoingeckoEndpoints(query_params=cfg.endpoint_query_params)

        self.formatter = CoingeckoDataFormatter()
        self.finder = CoingeckoDataFinder()
        self.cleaner = CoingeckoDataCleaner(datapoints=cfg.datapoints)

        self.config = cfg

        self.fetch = fetch_json
        self.scrape = scrape_url

        self._routine_interval_sec = cfg.routine_intervals_hours['1 hour'] * 360

        self._task = None

        self.routines = coingecko_routines_factory(coingecko_instance=self)
