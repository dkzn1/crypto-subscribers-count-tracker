from typing import Any
from datetime import datetime
from lib.base_classes.db_access_layer import DBAccessLayer

use_session = DBAccessLayer.use_session


class SubTrackerDBLayer(DBAccessLayer):
    """
    SubTrackerDBOperations is responsible for database operations related to social media subscriber routine data.
    """

    @use_session
    def save_subs_data(self, table_rows: list[dict[str, Any]], session={}) -> None:
        """
        Save social media subscriber data to the database.

        Args:
            table (CoinSocialMediaSubs): The table for storing social media subscriber data.
            table_rows (list[dict[str, Any]]): A list of dictionaries representing the data to be saved.

        Returns:
            None
        """
        today = datetime.now().date()

        table = self.models.CoinSocialMediaSubs

        subs = self.get_filtered_table(table, filter_condition=table.date == today)

        subs_dict = {row.id: row for row in subs}

        for row in table_rows:
            if row['id'] not in subs_dict:
                session.add(table(**row))
