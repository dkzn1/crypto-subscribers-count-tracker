from datetime import datetime
from lib.base_classes.routine import Routine

use_run_interval = Routine.run_interval_decorator


class TrendMonitorRoutine(Routine):
    """
    TrendMonitorRoutine class is responsible for running routines to monitor and find trends in social media subscribers data for coins.

    Methods:
        run: Executes the routine for monitoring coin subscriber trends.

    Private Methods:
        __find_trends: Finds trends for different time frames
    """

    @use_run_interval('24 hours')
    def run(self, _) -> None:
        """
        The main routine function to find and save trends for coins social media subscribers.

        Args:
            _: Placeholder for any unused arguments.
        """
        db = self._db

        social_subs = db.get_full_table(db.models.CoinSocialMediaSubs)

        f = self._formatter

        result = f.combine_sub_stats(social_subs)
        sub_stats = f.sort_sub_stats(result)

        coin_trends = self.__find_trends(sub_stats)

        trend_rows = f.create_trend_db_rows(coin_trends)

        db.save_trends(trend_rows)

        self._log.success()

    #
    #
    #

    def __find_trends(self, sub_stats: dict[str, dict[datetime, int]]) -> dict[str, dict[str, float]]:
        """
        Find trends in subscriber counts over different time periods.

        Args:
            sub_stats (dict): A dictionary containing subscriber count history for each coin.

        Returns:
            dict: A dictionary containing trends for each coin and time period.
        """
        p = self._processor

        def set_period_trends(days) -> dict[str, float]:
            trend = {}

            daily_subs = list(days.values())

            if len(daily_subs) > 2:
                trend['days_3'] = p.calc_percent_change(daily_subs, timeframe_end=2)

            if len(daily_subs) > 6:
                trend['days_7'] = p.calc_percent_change(daily_subs, timeframe_end=6)

            if len(daily_subs) > 13:
                trend['days_14'] = p.calc_percent_change(daily_subs, timeframe_end=13)

            if len(daily_subs) > 29:
                trend['days_30'] = p.calc_percent_change(daily_subs, timeframe_end=29)

            if len(daily_subs) > 59:
                trend['days_60'] = p.calc_percent_change(daily_subs, timeframe_end=59)

            if len(daily_subs) > 89:
                trend['days_90'] = p.calc_percent_change(daily_subs, timeframe_end=89)

            return trend

        coin_trends = {coin_id: set_period_trends(days) for coin_id, days in sub_stats.items()}

        return coin_trends
