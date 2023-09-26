from typing import Union
from lib.base_classes.db_access_layer import DBAccessLayer

use_session = DBAccessLayer.use_session


class TrendMonitorDBLayer(DBAccessLayer):
    """
    TrendMonitorDBOperations class handles database operations for saving trends for social media subscribers of coins.
    """

    @use_session
    def save_trends(self, trend_rows: list[dict[str, Union[str, float]]], session={}) -> None:
        """
        Save trend data in the database.

        Args:
            trend_rows (list): A list of dictionary rows containing trend data to be saved.
            session (dict, optional): A session dictionary for database operations (default is an empty dictionary).

        Returns:
            None
        """

        table = self.models.CoinSubscriberTrends

        session.query(table).delete()

        for row_data in trend_rows:
            session.add(table(**row_data))
