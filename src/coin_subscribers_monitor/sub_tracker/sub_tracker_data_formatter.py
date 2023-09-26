from typing import Union
from datetime import datetime
from functools import reduce

from lib.base_classes.processors.data_formatter import DataFormatter


class SubTrackerDataFormatter(DataFormatter):
    """
    SubTrackerDataFormatter is a data processor class that provides ulitity methods for formatting purposes for the SubTrackerRoutine.

    Methods:
        to_sub_table_rows: reate table rows for social media subscriber data.
    """

    @staticmethod
    #
    def to_sub_table_rows(sub_data: dict[str, dict[str, int]]) -> list[dict[str, Union[str, int]]]:
        """
        Create table rows for social media subscriber data for DB saving operation.

        Args:
            sub_data (dict): A dictionary containing coin IDs and their respective subscriber counts.

        Returns:
            list[dict]: A list of dictionaries representing subscriber data.
        """

        def create_platform_rows(result, sub_data):
            coin_id, coin_sub_data = sub_data

            today = datetime.now().strftime('%Y-%m-%d')

            for platform, sub_count in coin_sub_data.items():
                id = f'{coin_id}-{platform}-{today}'

                row = {"id": id, "coin_id": coin_id, 'platform_name': platform, 'subscriber_count': sub_count}

                result.append(row)

            return result

        platform_rows = reduce(create_platform_rows, sub_data.items(), [])

        return platform_rows
