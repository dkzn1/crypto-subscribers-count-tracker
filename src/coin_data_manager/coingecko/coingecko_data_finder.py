import json
from lib.base_classes.processors.data_finder import DataFinder
from models.unprocessed_coingecko_links import UnprocessedCoingeckoLinks


class CoingeckoDataFinder(DataFinder):
    """
    Data processor for Coingecko service data.

    This class provides methods to process and manipulate data retrieved from the Coingecko service.

    Attributes:
        datapoints (dict[str, Any]): A dictionary containing data points for processing.

    Methods:
        __init__: Initializes the CoingeckoDataProcessor.
        combine_coin_data: Combines data from 'toplist' and 'extended_toplist' responses for each coin.
        subdivide_toplist_data: Subdivides data points from the 'toplist' response into 'base_data' and 'market_data'.
        subdivide_extended_toplist_data: Subdivides data points from the 'extended_toplist' response into different categories.
        extract_coin_homepages: Extracts coin homepages from the 'links' data.
    """

    @staticmethod
    #
    def extract_coin_homepages(unprocessed_links: list[UnprocessedCoingeckoLinks]) -> list[dict[str, str]]:
        """
        Extracts coin homepages from the 'links' data.

        Args:
            unprocessed_links (list[UnprocessedCoingeckoLinks]): List of unprocessed Coingecko links.

        Returns:
            list[dict[str, str]]: List of dictionaries containing coin IDs and homepage URLs.
        """

        def create_homepage_dict(coin_data):
            links = json.loads(coin_data.links)

            homepages = list(filter(lambda item: item != "", links['homepage']))

            return {'coin_id': coin_data.coin_id, 'homepage_url': homepages[0]}

        coins_homepages = [create_homepage_dict(coin_data) for coin_data in unprocessed_links]

        return coins_homepages
