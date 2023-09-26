from typing import Union


class Config:
    """
    Configuration class that defines various constants and settings for the project.

    This class includes configuration options such as routine intervals in hours and refetch timeout in seconds.

    Attributes:
        routine_intervals_hours (dict[str, Union[int, float]]): A dictionary mapping routine intervals (e.g., '5 min')
            to their corresponding time in hours.
        refetch_timeout_sec (int): The timeout in seconds used for refetching data.

    """

    routine_intervals_hours: dict[str, Union[int, float]] = {
        '5 min': 0.1,
        '10 min': 0.15,
        '12 min': 0.2,
        '15 min': 0.25,
        '1 hour': 1,
        '12 hours': 12,
        '24 hours': 24,
        '2 days': 48,
        '3 days': 72,
    }

    refetch_timeout_sec: int = 20
