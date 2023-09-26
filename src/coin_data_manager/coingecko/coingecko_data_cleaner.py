from typing import Any, Union
from lib.base_classes.processors.data_cleaner import DataCleaner
from models.stablecoin import Stablecoin


class CoingeckoDataCleaner(DataCleaner):
    """
    Data Cleaner for filtering and removing redundant data from Coingecko service.

    This class provides methods to filter and process data retrieved from the Coingecko service based on specific criteria.

    Attributes:
        datapoints (dict[str, Any]): A dictionary containing data points for processing.

    Methods:
        filter_coin_datapoints: Filters coin data points based on the specified list type.
        filter_out_stablecoins: Filters out stablecoins from the toplist.
        __filter_nested_coin_datapoints: Filters nested coin data points based on specified data points.
    """

    def __init__(self, datapoints: dict[str, Any]) -> None:
        """
        Initialize the CoingeckoDataProcessor.

        Args:
            datapoints (dict[str, Any]):
            A dictionary containing data points for processing.
        """
        self.datapoints = datapoints

    #
    #
    #

    def filter_coin_datapoints(self, coin_list: list[dict[str, Union[str, int, float]]], list_type: str) -> list[dict[str, Union[str, int, float]]]:
        """
        Filters coin data points based on the specified list type.

        Args:
            coin_list (list[dict[str, Union[str, int, float]]]): A list of coin data dictionaries.
            list_type (str): The type of data points to filter.

        Returns:
            list[dict[str, Union[str, int, float]]]: A list of filtered coin data dictionaries.
        """

        def set_key(key) -> str:
            return 'coin_id' if key == 'id' else key

        def filter_coin_data(coin_data):
            #
            result = {set_key(key): value for key, value in coin_data.items() if key in self.datapoints[list_type]}

            if list_type == 'extended_toplist':
                nested_result = self.__filter_nested_coin_datapoints(result, self.datapoints['extended_toplist_nested'])

                return nested_result

            return result

        processed_list = [filter_coin_data(coin_data) for coin_data in coin_list]

        return processed_list

    #
    #
    #

    @staticmethod
    #
    def filter_out_stablecoins(toplist: list[dict[str, Union[str, int, float]]], stablecoins: list[Stablecoin]) -> list[dict[str, Union[str, int, float]]]:
        """
        Filters out stablecoins from the toplist.

        Args:
            toplist (list[dict[str, Union[str, int, float]]]): A list of top coin data dictionaries.
            stablecoin_ids (list[str]): A list of stablecoin IDs.

        Returns:
            list[dict[str, Union[str, int, float]]]: A list of filtered top coin data dictionaries.
        """
        stablecoin_ids: list[str] = [stablecoin.coin_id for stablecoin in stablecoins]

        filtered_toplist = [coin for coin in toplist if coin["coin_id"] not in stablecoin_ids]

        return filtered_toplist

    #
    #
    #

    @staticmethod
    #
    def __filter_nested_coin_datapoints(nested_coin_data: dict[str, Any], datapoints: dict[str, list[str]]) -> dict[str, Any]:
        """
        Filters nested coin data points based on the specified data points.

        Args:
            nested_coin_data (dict[str, Any]): A dictionary of nested coin data.
            datapoints (dict[str, list[str]]): A dictionary of data points to filter.

        Returns:
            dict[str, Any]: A dictionary of filtered nested coin data.
        """

        def filter_nested_coin_data(key: str, data: dict[str, Any]):
            #
            if key not in datapoints:
                return data

            nested_result = {nested_key: value for nested_key, value in data.items() if nested_key in datapoints[key]}

            return nested_result

        result = {key: filter_nested_coin_data(key, value) for key, value in nested_coin_data.items()}

        return result
