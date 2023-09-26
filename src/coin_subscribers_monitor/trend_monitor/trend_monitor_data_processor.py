from lib.base_classes.processors.data_processor import DataProcessor


class TrendMonitorProcessor(DataProcessor):
    """
    TrendMonitorProcessor class is responsible for offering processing methods needed to find trends in social media subscriber data.
    """

    @staticmethod
    #
    def calc_percent_change(daily_subs, timeframe_end, timeframe_start=0):
        """
        Calculate the percentage change in subscriber count over a specified timeframe.

        Args:
            daily_subs (list): A list of daily subscriber counts.
            timeframe_end (int): The ending day of the timeframe.
            timeframe_start (int): The starting day of the timeframe (default is 0).

        Returns:
            float: The calculated net percentage change.
        """
        difference_percent = round(daily_subs[timeframe_end] / daily_subs[timeframe_start], 3)
        net_percent = round(1 - difference_percent, 3)
        return net_percent
