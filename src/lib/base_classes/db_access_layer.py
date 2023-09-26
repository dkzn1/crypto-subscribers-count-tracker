from typing import Any, Callable

from db.session_decorator import session_decorator


class DBAccessLayer:
    """
    A utility class for common database operations with SQLAlchemy.

    This class provides methods to interact with database tables including fetching data, filtering data,
    and saving data to a specified table.

    Attributes:
        use_session (Callable): A decorator function for database session management.

    Args:
        db: The database instance with an SQLAlchemy engine and model definitions.

    """

    use_session: Callable = session_decorator

    def __init__(self, db) -> None:
        """
        Initializes the DatabaseOperations instance.

        Args:
            db: The database instance containing an SQLAlchemy engine and model definitions.

        """
        self.engine = db.engine
        self.models = db.models

    #
    #
    #

    @use_session
    def get_full_table(self, table, session={}) -> list[Any]:
        """
        Retrieve all rows from a specified database table.

        Args:
            table: The database table class to fetch data from.
            session: The database session (provided by the session_decorator).

        Returns:
            list[Any]: A list of rows from the specified table.

        """
        response = session.query(table).all()

        return response

    #
    #
    #

    @use_session
    def get_filtered_table(self, table, filter_condition=None, session={}) -> list[Any]:
        """
        Retrieve rows from a specified database table based on a filter condition.

        Args:
            table: The database table class to fetch data from.
            filter_condition: An optional filter condition to narrow down the selection.
            session: The database session (provided by the session_decorator).

        Returns:
            list[Any]: A list of rows from the specified table that match the filter condition.

        """
        response = session.query(table).filter(filter_condition).all()

        return response

    #
    #
    #

    @use_session
    def save_table_data(self, table, table_rows: list[dict[str, Any]], session={}) -> None:
        """
        Save a list of row data to a specified database table.

        Args:
            table: The database table class to which data will be saved.
            table_rows: A list of dictionaries containing data for each row.
            session: The database session (provided by the session_decorator).

        """
        for row_data in table_rows:
            session.add(table(**row_data))
