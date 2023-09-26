from functools import reduce
from datetime import datetime
from lib.base_classes.processors.data_formatter import DataFormatter

from models.coin_social_media_subs import CoinSocialMediaSubs


class TrendMonitorFormatter(DataFormatter):
    """
    TrendMonitorFormatter class is responsible for offering formatting methods needed to find trends in social media subscriber data.
    """

    @staticmethod
    #
    def combine_sub_stats(social_subs: list[CoinSocialMediaSubs]) -> dict[str, dict[datetime, int]]:
        """
        Combine and aggregate social media subscriber data by coin and date.

        Args:
            social_subs (list): A list of social media subscriber data rows.

        Returns:
            dict: A dictionary containing aggregated subscriber data for each coin and date.
        """

        def create_total_subs_per_day(result, row):
            coin_id, date = row.coin_id, row.date

            if coin_id not in result:
                result[coin_id] = {}

            if date not in result[coin_id]:
                result[coin_id][date] = 0

            result[coin_id][date] += row.subscriber_count

            return result

        total_subs = reduce(create_total_subs_per_day, social_subs, {})

        return total_subs

    #
    #
    #

    @staticmethod
    #
    def sort_sub_stats(sub_stats) -> dict[str, dict[datetime, int]]:
        """
        Sort social media subscriber data by date in descending order.

        Args:
            sub_stats (dict): A dictionary containing aggregated subscriber data for each coin and date.

        Returns:
            dict: A dictionary containing sorted subscriber data for each coin.
        """

        def sort_by_dates_desc(coin_id) -> dict[datetime, int]:
            return dict(sorted(sub_stats[coin_id].items(), reverse=True))

        sorted_subs = {coin_id: sort_by_dates_desc(coin_id) for coin_id in sub_stats.keys()}

        return sorted_subs

    #
    #
    #

    @staticmethod
    #
    def create_trend_db_rows(trends: dict[str, dict[str, float]]) -> list[dict[str, float]]:
        """
        Create database rows for trends in social media subscribers.

        Args:
            trends (dict[str, dict[str, float]]): A dictionary containing trends for each coin.

        Returns:
            list[dict[str, float]]: A list of database rows containing trend data.
        """
        rows = [{"coin_id": coin_id, **trend_data} for coin_id, trend_data in trends.items()]

        return rows
