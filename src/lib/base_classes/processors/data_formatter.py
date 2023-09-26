from lib.interfaces.data_processor_interface import IDataProcessor
from models.base import Base as SqlTable


class DataFormatter(IDataProcessor):
    """
    Base class for processing data that falls under formatting category.

    This class provides a foundation for data processors and defines a common utility methods for formatting data in different services.

    Methods:
        __init__: Initializes the DataProcessorBase class. To be implemented in subclasses.
        to_table_by_coin_id_index: Creates a dictionary from a list of SQL table objects.
    """

    def __init__(self) -> None:
        """
        Initialize the DataFormatter.

        Implement in subclasses.
        """
        pass

    #
    #
    #

    @staticmethod
    #
    def to_table_by_coin_id_index(table: list[SqlTable]) -> dict[str, SqlTable]:
        """
        Creates a dictionary index from a list of SQL table objects by.

        Args:
            table (list[SqlTable]): A list of SQL table objects.

        Returns:
            dict[str, SqlTable]: A dictionary mapping a unique identifier (e.g., coin_id) to its corresponding SQL table object.
        """
        return {coin.coin_id: coin for coin in table}
