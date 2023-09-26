from typing import Union


class CoingeckoEndpoints:
    '''
    Representing endpoints used for making requests to the CoinGecko API.

    Args:
        query_params (dict[str, Union[str, int]]): Configuration settings for the endpoints.

    Attributes:
        query_params (dict[str, Union[str, int]]): Configuration settings for the endpoints.
    '''

    def __init__(self, query_params: dict[str, Union[str, int]]) -> None:
        """
        Initialize a CoingeckoEndpoints instance.

        Args:
            query_params (dict[str, Union[str, int]]): Configuration settings for the endpoints.
        """
        self.query_params = query_params

    #
    #
    #

    ping_endpoint: str = 'https://api.coingecko.com/api/v3/ping'

    #

    stablecoins_endpoint: str = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&category=stablecoins&order=market_cap_desc&per_page=250&page=1&sparkline=false&locale=en'

    #
    #
    #

    def create_toplist_endpoint(self) -> str:
        """
        Create a URL for the toplist endpoint.

        Returns:
            str: The URL for the toplist endpoint based on the configuration settings.
        """
        return f'https://api.coingecko.com/api/v3/coins/markets?vs_currency={self.query_params["currency"]}&order=market_cap_desc&per_page={self.query_params["toplist_len"]}&page=1&sparkline=false&price_change_percentage=1h%2C24h%2C7d%2C14d%2C30d%2C200d%2C1y&locale=en'

    #
    #
    #

    def create_coin_data_endpoint(self, coin_id) -> str:
        """
        Create a URL for a specific coin's extended data endpoint.

        Args:
            coin_id (str): The ID of the coin.

        Returns:
            str: The URL for the coin's extended data endpoint.
        """

        return f'https://api.coingecko.com/api/v3/coins/{coin_id}?localization=false&tickers=false&market_data=false&community_data=true&developer_data=true&sparkline=false'
