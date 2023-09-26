from typing import Any, Union
from functools import reduce
import json

from lib.base_classes.processors.data_formatter import DataFormatter


class CoingeckoDataFormatter(DataFormatter):
    """
    Data formatter class to support coingecko service operations with utility functions for data formatting.


    Methods:
        - combine_coin_data(toplist, extended_toplist)
        - subdivide_toplist_data(toplist)
        - subdivide_extended_toplist_data(extended_toplist)
    """

    @staticmethod
    #
    def combine_coin_data(toplist: list[dict[str, Any]], extended_toplist: list[dict[str, Any]]) -> dict[str, Any]:
        """
        Combines data from 'toplist' and 'extended_toplist' responses for each coin.

        Args:
            toplist (list[dict[str, Any]]): List of data points from the 'toplist' response.
            extended_toplist (list[dict[str, Any]]): List of data points from the 'extended_toplist' response.

        Returns:
            dict[str, Any]: Combined data for each coin.
        """

        def combine_data(result, toplist_coin_data):
            coin_id = toplist_coin_data['id']

            extended_data = [coin_data for coin_data in extended_toplist if coin_data['id'] == coin_id]

            if len(extended_data) > 0:
                result[coin_id] = {**toplist_coin_data, **extended_data[0]}

                del result[coin_id]['links']
                extended_toplist.remove(extended_data[0])

            return result

        combined_data_list = reduce(combine_data, toplist, {})

        return combined_data_list

    #
    #
    #

    @staticmethod
    #
    def subdivide_toplist_data(toplist: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
        """
        Subdivides data points from the 'toplist' response into 'base_data' and 'market_data' for db saving operation.

        Args:
            toplist (list[dict[str, Any]]): List of data points from the 'toplist' response.

        Returns:
            list[list[dict[str, Any]]]: Subdivided 'base_data' and 'market_data'.
        """

        def split_datatypes(result, coin_data) -> dict[str, list]:
            base_data = {}
            market_data = {}

            for key, value in coin_data.items():
                if key == 'coin_id':
                    base_data[key] = value

                if key in ('symbol', 'name'):
                    base_data[key] = value
                else:
                    market_data[key] = value

            result['base_data'].append(base_data)
            result['market_data'].append(market_data)

            return result

        result = reduce(split_datatypes, toplist, {'base_data': [], 'market_data': []})

        return [result['base_data'], result['market_data']]

    #
    #
    #

    @staticmethod
    #
    def subdivide_extended_toplist_data(extended_toplist: list[dict[str, Any]]) -> list[dict[str, dict[str, Union[str, int, float]]]]:
        """
        Subdivides data points from the 'extended_toplist' response into different categories for db saving operation.

        Args:
            extended_toplist (list[dict[str, Any]]): List of data points from the 'extended_toplist' response.

        Returns:
            list[dict[str, dict[str, Union[str, int, float]]]]: Subdivided data for each coin.
        """

        def split_datatypes(coin_data):
            row_data = {'categories': {}, 'ratings': {}, 'unprocessed_links': {}}

            for key, value in coin_data.items():
                if key == 'coin_id':
                    row_data['categories'][key] = value
                    row_data['ratings'][key] = value
                    row_data['unprocessed_links'][key] = value

                elif key == 'categories':
                    category_string = ";".join(value)
                    row_data['categories'][key] = category_string

                elif key == 'links':
                    links_dict_string = json.dumps(value)
                    row_data['unprocessed_links'][key] = links_dict_string

                else:
                    row_data['ratings'][key] = value

            return row_data

        result = [split_datatypes(coin_data) for coin_data in extended_toplist]

        return result
