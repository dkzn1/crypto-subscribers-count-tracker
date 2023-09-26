from typing import Union, Any
import time
from lib.base_classes.routine import Routine


use_run_interval = Routine.run_interval_decorator


def coingecko_routines_factory(coingecko_instance) -> dict[str, Routine]:
    """
    Creates and returns a dictionary of Coingecko-related routines.

    This function initializes routine instances for handling different Coingecko-related tasks and returns them as a dictionary.

    Args:
        coingecko_instance (CoingeckoCoordinator): An instance of CoingeckoCoordinator for service coordination.

    Returns:
        dict[str, RoutineBase]: A dictionary mapping routine names to their corresponding routine instances.

    Example Usage:
        routines = coingecko_routines_factory(coingecko_instance)
        toplist_routine = routines["ToplistRoutine"]
        toplist_routine.run()
    """
    routines = {}

    routines['StablecoinsRoutine'] = StablecoinsRoutine(coingecko_instance)
    routines['ToplistRoutine'] = ToplistRoutine(coingecko_instance)
    routines['ExtendedToplistRoutine'] = ExtendedToplistRoutine(coingecko_instance)
    routines['HomepageRoutine'] = HomepageRoutine(coingecko_instance)

    return routines


#


class ToplistRoutine(Routine):
    """
    Routine for fetching and processing top cryptocurrency data from the Coingecko API.

    This routine fetches toplist data from the API, processes it, and saves it to the database.

    Attributes:
        None

    Methods:
        run: Executes the routine, fetching and processing data from the API.

    Example Usage:
        toplist_routine = ToplistRoutine(service, processor, db)
        toplist_routine.run()
    """

    @use_run_interval('1 hour')
    def run(self, refetch_attempts: int = 4) -> None:
        """
        Execute the routine to fetch and process top cryptocurrency data.

        Args:
            refetch_attempts (int): The number of refetch attempts in case of API failure (default: 4).
        """
        coingecko = self._service

        endpoint = coingecko.endpoints.create_toplist_endpoint()
        response = coingecko.fetch(endpoint)

        if response:
            c = self._cleaner
            db = self._db

            toplist = c.filter_coin_datapoints(coin_list=response, list_type='toplist')

            stablecoins = db.get_full_table(table=db.models.Stablecoin)

            pure_toplist = c.filter_out_stablecoins(toplist, stablecoins)

            base_data, market_data = self._formatter.subdivide_toplist_data(pure_toplist)

            db.save_base_data(base_data)
            db.save_market_data(market_data)

            self._log.success()

        else:
            self._refetch(self.run, self._refetch_timeout_sec, refetch_attempts)

            if refetch_attempts == 0:
                self._log.warn('fetch_failure')


#


class StablecoinsRoutine(Routine):
    """
    Routine for fetching and processing stablecoins data from the Coingecko API.

    This routine fetches stablecoin data from the API, processes it, and saves it to the database.

    Attributes:
        None

    Methods:
        run: Executes the routine, fetching and processing data from the API.

    Example Usage:
        stablecoins_routine = StablecoinsRoutine(service, db)
        stablecoins_routine.run()
    """

    @use_run_interval('3 days')
    def run(self, refetch_attempts: int = 4) -> None:
        """
        Execute the routine to fetch and process stablecoins data.

        Args:
            refetch_attempts (int): The number of refetch attempts in case of API failure (default: 4).
        """
        coingecko = self._service

        endpoint = coingecko.endpoints.stablecoins_endpoint
        response = coingecko.fetch(endpoint)

        if response:
            stablecoins_data = [{"coin_id": coin["id"]} for coin in response]
            self._db.save_stablecoins(stablecoins_data)
            self._log.success()

        else:
            self._refetch(self.run, self._refetch_timeout_sec, refetch_attempts)

            if refetch_attempts == 0:
                self._log.warn('fetch_failure')


#


class ExtendedToplistRoutine(Routine):
    """
    Routine for fetching and processing extended toplist cryptocurrency data from the Coingecko API.

    This routine fetches extended toplist data from the API, processes it, and saves it to the database.

    Attributes:
        None

    Methods:
        run: Executes the routine, fetching and processing data from the API.

    Example Usage:
        extended_toplist_routine = ExtendedToplistRoutine(service, processor, db)
        extended_toplist_routine.run()
    """

    @use_run_interval('24 hours')
    def run(self, _) -> None:
        """
        Execute the routine to fetch and process extended toplist cryptocurrency data.

        Args:
            _ (Unused): Placeholder argument.
        """
        coingecko = self._service
        db = self._db

        self._insufficient_data: bool = False

        result = db.get_full_table(db.models.CoinBaseData.coin_id)
        coin_ids: list[str] = [coin.coin_id for coin in result]

        response = [self.__fetch_coin(coingecko, coin_id) for coin_id in coin_ids[0:10]]

        if self._insufficient_data:
            self._log.warn('insufficient')

            return

        extended_toplist = self._cleaner.filter_coin_datapoints(coin_list=response, list_type='extended_toplist')

        seperated_coinlist = self._formatter.subdivide_extended_toplist_data(extended_toplist)

        db.save_extended_toplist_data(seperated_coinlist)

        self._log.success()

    #
    #
    #

    def __fetch_coin(self, coingecko, coin_id: str, refetch_attempts: int = 4) -> dict[str, Union[dict[str, Any], dict]]:
        """
        Fetches extended data for a specific coin from the Coingecko API.

        Args:
            coingecko (CoingeckoCoordinator): An instance of the CoingeckoCoordinator for API access.
            coin_id (str): The ID of the coin to fetch data for.
            refetch_attempts (int): The number of refetch attempts in case of API failure (default: 4).

        Returns:
            dict[str, Union[dict[str, Any], dict]]: The extended data for the specified coin.

        Raises:
            Exception: If the data cannot be fetched after all refetch attempts.
        """
        response = coingecko.fetch(coingecko.endpoints.create_coin_data_endpoint(coin_id))

        if response:
            time.sleep(coingecko.config.request_delay_time_seconds)
            return response

        elif refetch_attempts == 0:
            self._insufficient_data = True
            return {}

        else:
            return self.__fetch_coin(coingecko, coin_id, refetch_attempts - 1)


#


class HomepageRoutine(Routine):
    """
    Routine for extracting and saving coin homepages.

    This routine extracts and saves coin homepages to the database.

    Attributes:
        None

    Methods:
        run: Executes the routine, extracting and saving coin homepages.

    Example Usage:
        homepage_routine = HomepageRoutine(processor, db)
        homepage_routine.run()
    """

    @use_run_interval('2 days')
    def run(self, _) -> None:
        """
        Execute the routine to extract and save coin homepages.

        Args:
            _ (Unused): Placeholder argument.
        """

        db = self._db

        raw_links_data = db.get_full_table(db.models.UnprocessedCoingeckoLinks)

        existing_homepages_index = self._formatter.to_table_by_coin_id_index(db.get_full_table(db.models.CoinHomepageLink))

        updates = [links for links in raw_links_data if links.coin_id not in existing_homepages_index]

        coin_homepages = self._finder.extract_coin_homepages(updates)

        db.save_coin_homepages(coin_homepages)

        self._log.success()
