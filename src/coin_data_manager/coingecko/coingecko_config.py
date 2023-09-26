from typing import Union
from lib.base_classes.config import Config


class CoingeckoConfig(Config):
    """
    Configuration settings for interacting with the Coingecko API.

    This class defines the configuration parameters for making requests to the Coingecko API.

    Attributes:
        endpoint_query_params (dict): Default query parameters for API endpoints.
            - 'currency': The currency to use for pricing information (default: 'usd').
            - 'toplist_len': The number of top cryptocurrencies to retrieve (default: 250).

        request_delay_time_seconds (int): The delay time in seconds between consecutive API requests (default: 7).

        datapoints (dict): Defines the data points to retrieve for different API endpoints.
            - 'toplist': List of data points to retrieve for the top cryptocurrencies.
            - 'stablecoins': List of data points to retrieve for stablecoins.
            - 'extended_toplist': List of data points to retrieve for extended top cryptocurrency data.
            - 'extended_toplist_nested': Nested data points to retrieve for extended top cryptocurrency data.
    """

    endpoint_query_params: dict[str, Union[str, int]] = {
        'currency': 'usd',
        'toplist_len': 250,
    }

    request_delay_time_seconds: int = 7

    datapoints: dict[str, Union[list[str], dict[str, list[str]]]] = {
        'toplist': [
            "id",
            "symbol",
            "name",
            "current_price",
            "market_cap",
            "market_cap_rank",
            "total_volume",
            "high_24h",
            "low_24h",
            "last_updated",
            "price_change_percentage_1h_in_currency",
            "price_change_percentage_24h_in_currency",
            "price_change_percentage_7d_in_currency",
            "price_change_percentage_14d_in_currency",
            "price_change_percentage_30d_in_currency",
            "price_change_percentage_200d_in_currency",
            "price_change_percentage_1y_in_currency",
        ],
        'stablecoins': [
            "id",
        ],
        'extended_toplist': [
            "id",
            "categories",
            "links",
            "watchlist_portfolio_users",
            "coingecko_score",
            "developer_score",
            "community_score",
            "liquidity_score",
            "public_interest_score",
        ],
        'extended_toplist_nested': {
            "links": ["homepage", "telegram_channel_identifier", "subreddit_url", "repos_url", "chat_url", "chat_url"],
            "developer_data": ["forks", "stars", "subscribers", "total_issues", "pull_requests_merged", "pull_request_contributors", "commit_count_4_weeks"],
        },
    }
